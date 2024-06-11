# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

# Import libraries
import os, sys, toml

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api, neucol

from typing import Optional
import fire, transformers, torch
from alive_progress import alive_bar


def main(
    filemap: str,
    template: str,
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

    mapping = neucol.create_src_mapping(filemap)

    source_files = mapping["src"]["files"]
    target_files = mapping["dest"]["files"]

    if len(source_files) != len(target_files):
        api.display_output(
            "source_files and target_files for conversion do not match in length"
        )
        raise ValueError

    api.display_output(f'Loading template from "{template}"')
    instructions = toml.load(template)["instructions"]

    api.display_output("Starting code conversion process")

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

                source_code = []
                with open(sfile, "r") as source:
                    for line in source.readlines():
                        if len(line.strip()) > 2:
                            if (
                                line.strip()[0] != "!"
                                and line.strip()[:2] != "/*"
                                and line.strip()[:2] != "//"
                            ):
                                source_code.append(line)
                        else:
                            source_code.append(line)

                with open(tfile, "w") as destination:
                    destination.write("/* LLM INSTRUCTIONS START\n")
                    for line in instructions[0]["content"].split("\n"):
                        destination.write(f" * {line}\n")
                    destination.write(f" * LLM INSTRUCTIONS END */\n\n")

                    saved_prompt = instructions[-1]["content"]
                    instructions[-1]["content"] += "\n" + "".join(source_code)

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
                    instructions[-1]["content"] = saved_prompt

            else:
                continue


if __name__ == "__main__":
    fire.Fire(main)
