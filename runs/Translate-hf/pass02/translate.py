# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

# Import libraries
import os, sys

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api, neucol

from typing import Optional
import fire, transformers, torch
from alive_progress import alive_bar


def main(
    max_new_tokens: int = 4096,
    batch_size: int = 8,
    max_length: Optional[int] = None,
):

    llm_choice = api.get_user_input(
        f"LLM powered code conversion tool that uses the transformers API "
        + f"to test different models.\n\t1. mistral-7b\n\t2. codellama-7b\n\t3. gemma-7b\nSelect "
        + f"the model you would like to interact with"
    )

    if int(llm_choice) == 1:
        ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "mistral/Mistral-7B-Instruct-v0.1"
    elif int(llm_choice) == 2:
        ckpt_dir = (
            os.getenv("MODEL_HOME") + os.sep + "codellama/CodeLlama-7b-Instruct-hf"
        )
    elif int(llm_choice) == 3:
        ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "google/gemma-7b-it"
    else:
        api.display_output(f"Option {llm_choice} not defined")
        raise NotImplementedError

    if not os.path.exists(ckpt_dir):
        api.display_output(
            f'Checkpoint directory does not exist for option "{llm_choice}"'
        )
        raise NotImplementedError
    else:
        api.display_output(f'Checkpoint directory exists for option "{llm_choice}"')

    dest = api.get_user_input("Enter destination folder name")
    mapping = neucol.create_src_mapping(dest)

    source_dirs = api.get_user_input(
        "Enter source code directories separated by commas, use (*) for all"
    )
    source_files = []
    target_files = []

    if source_dirs == "*":
        source_files.extend(mapping["src"]["files"])
        target_files.extend(mapping["dest"]["files"])

    else:
        for sfile, tfile in zip(mapping["src"]["files"], mapping["dest"]["files"]):
            for sdir in source_dirs.split(","):
                if (sdir.strip() in sfile) and (sdir.strip() in tfile):
                    source_files.append(sfile)
                    target_files.append(tfile)

    if len(source_files) != len(target_files):
        api.display_output(
            "source_files and target_files for conversion do not match in length"
        )
        raise ValueError

    api.display_output("Starting code conversion process")

    main_prompt = []
    main_prompt.append(
        "- You are a code conversion tool for a scientific computing application. "
        + "The application is organized as different source files in a directory structure."
    )
    main_prompt.append(
        "- Convert this file to a C++ source code file. Note that inputs are chunks which belong to same file, do not try "
        + "to infer around the input or provide any context. Simply convert the source code from FORTRAN to C++."
    )
    main_prompt.append(
        "- I am writing the output directly to a source file so make sure whatever I receive from you is a "
        + "compilable C++ syntax. This means any comments you make on the code or conversion process should be included "
        + "as a C++ comment. Any text that is not code should be include as a C++ commment. Do not use a markdown format"
    )
    main_prompt.append(
        "- The code blocks you will receive are part of a bigger codebase so do not add "
        + "additional function declarations, or a main function definition. Just do the conversion process line-by-line."
    )
    main_prompt.append(
        ' - Change "use <module-name>" statement to C++ "using namespace <module-name>" and include the corresponding header '
        + 'file with the same name.For example "use types" should be replaced with "#include "types.hpp"" and '
        + '"using namespace types". Additionally, Treat "module <module-name> ... end <module-name>" as separate namespace.'
    )
    main_prompt.append(
        '- Put the "#include" statements at the top of the file and assume that any '
        + "variables that are not declared in the file are available in the header file."
    )
    main_prompt.append(
            '- Treat "real(dp)" as "std::double", and "complex(dp)" as "std::complex<double>" to convert to '
            + 'corresponding C++ types. Adjust the syntax for correctness.'
    )

    tokenizer = transformers.AutoTokenizer.from_pretrained(ckpt_dir)

    pipeline = transformers.pipeline(
        "text-generation",
        model=ckpt_dir,
        torch_dtype=torch.float16,
        device=0,
    )

    with alive_bar(len(source_files), bar="blocks") as bar:

        for sfile, tfile in zip(source_files, target_files):

            bar.text(sfile.replace(mapping["src"]["dir"] + os.sep, ""))
            bar()

            if not os.path.isfile(tfile):

                with open(sfile, "r") as source:
                    source_code = source.readlines()

                file_prompt = neucol.infer_src_mapping(sfile, mapping)
                file_prompt.append("The following code is part of a single file")

                llm_prompt = main_prompt + file_prompt

                with open(tfile, "w") as destination:
                    destination.write("/*PROMPT START")
                    for prompt_line in llm_prompt:
                        destination.write(f"\n// {prompt_line}")
                    destination.write(f"\nPROMPT END*/\n\n")

                    instructions = [
                        dict(
                            role="user",
                            content="\n".join(llm_prompt)
                            + ":\n"
                            + "".join(source_code),
                        )
                    ]

                    results = pipeline(
                        instructions,
                        max_new_tokens=max_new_tokens,
                        max_length=max_length,
                        batch_size=batch_size,
                        # temperature=temperature,
                        # top_p=top_p,
                        # do_sample=True,
                        eos_token_id=tokenizer.eos_token_id,
                        pad_token_id=50256,
                    )

                    for result in results:
                        destination.write(result["generated_text"][-1]["content"])
                        # code_block_indices = []
                        # for index, line in enumerate(output_lines):
                        #    if line[:2] == "```":
                        #        code_block_indices.append(index)
                        #
                        # if len(code_block_indices) > 2:
                        #    api.display_output(
                        #        "More than one code blocks in LLM output"
                        #    )
                        #    raise NotImplementedError
                        #
                        # for index, line in enumerate(output_lines):
                        #    if (
                        #        index < code_block_indices[0]
                        #        or index > code_block_indices[1]
                        #    ):
                        #        destination.write(f'// {line}"\n"')
                        #    else:
                        #        destination.write(f'{line}"\n"')

            else:
                continue


if __name__ == "__main__":
    fire.Fire(main)
