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

    #llm_choice = api.get_user_input(
    #    f"LLM powered code conversion tool that uses the transformers API "
    #    + f"to test different models.\n\t1. mistral-7b\n\t2. codellama-7b\n\t3. gemma-7b\nSelect "
    #    + f"the model you would like to interact with"
    #)

    #if int(llm_choice) == 1:
    #    ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "mistral/Mistral-7B-Instruct-v0.1"
    #elif int(llm_choice) == 2:
    #    ckpt_dir = (
    #        os.getenv("MODEL_HOME") + os.sep + "codellama/CodeLlama-7b-Instruct-hf"
    #    )
    #elif int(llm_choice) == 3:
    #    ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "google/gemma-7b-it"
    #else:
    #    api.display_output(f"Option {llm_choice} not defined")
    #    raise NotImplementedError
    #
    #if not os.path.exists(ckpt_dir):
    #    api.display_output(
    #        f'Checkpoint directory does not exist for option "{llm_choice}"'
    #    )
    #    raise NotImplementedError
    #else:
    #    api.display_output(f'Checkpoint directory exists for option "{llm_choice}"')

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

    # tokenizer = transformers.AutoTokenizer.from_pretrained(ckpt_dir)
    #
    # pipeline = transformers.pipeline(
    #    "text-generation",
    #    model=ckpt_dir,
    #    torch_dtype=torch.float16,
    #    device=0,
    # )

    with alive_bar(len(source_files), bar="blocks") as bar:

        for sfile, tfile in zip(source_files, target_files):

            bar.text(sfile.replace(mapping["src"]["dir"] + os.sep, ""))
            bar()

            if not os.path.isfile(tfile):

                with open(sfile, "r") as source:
                    source_code = source.readlines()

                with open(tfile, "w") as destination:
                    if tfile.endswith((".f")) and any(
                        module in tfile for module in ["ThreeJets"]
                    ):
                        new_source_code = []
                        for line in source_code:
                            if not "use" in line.strip():
                                new_source_code.append(line)

                        source_code = new_source_code
                        new_source_code = []
                        for line in source_code:
                            if "implicit none" in line.strip():
                                new_source_code.append(line)
                                new_source_code.append('      include"AllModules.h"\n')
                            else:
                                new_source_code.append(line)

                        destination.write("".join(new_source_code))
                    else:
                        destination.write("".join(source_code))
            else:
                continue


if __name__ == "__main__":
    fire.Fire(main)
