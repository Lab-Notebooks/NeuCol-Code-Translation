# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

# Import libraries
from typing import Optional
import fire
import transformers
import torch
import json
from types import SimpleNamespace
import os, glob

Color = SimpleNamespace(
    purple="\033[95m",
    cyan="\033[96m",
    darkcyan="\033[36m",
    blue="\033[94m",
    green="\033[92m",
    yellow="\033[93m",
    red="\033[91m",
    bold="\033[1m",
    underline="\033[4m",
    end="\033[0m",
)


def main(
    max_new_tokens: int = 4096,
    batch_size: int = 8,
    max_length: Optional[int] = None,
):

    torch.cuda.empty_cache()
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:25"

    choice = input(
        f"{Color.darkcyan}LLM powered code conversion tool that uses the transformers API "
        + f"to test different models.\n\t1. mistral-7b\n\t2. codellama-7b\n\t3. gemma-7b\nSelect "
        + f"the model you would like to interact with: "
    )

    print(f"{Color.end}")

    if int(choice) == 1:
        ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "mistral/Mistral-7B-Instruct-v0.1"
    elif int(choice) == 2:
        ckpt_dir = (
            os.getenv("MODEL_HOME") + os.sep + "codellama/CodeLlama-7b-Instruct-hf"
        )
    elif int(choice) == 3:
        ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "google/gemma-7b-it"
    else:
        raise ValueError(f"Option {choice} not defined")

    dest_dir = os.getenv("MCFM_HOME") + os.sep + "src_cpp"
    src_dir = os.getenv("MCFM_HOME") + os.sep + "src"

    if not os.path.exists(dest_dir + os.sep + "Mods"):
        os.makedirs(dest_dir + os.sep + "Mods")

    if not os.path.exists(dest_dir + os.sep + "ThreeJets"):
        os.makedirs(dest_dir + os.sep + "ThreeJets")

    tokenizer = transformers.AutoTokenizer.from_pretrained(ckpt_dir)

    pipeline = transformers.pipeline(
        "text-generation",
        model=ckpt_dir,
        torch_dtype=torch.float16,
        device=0,
    )

    while True:

        source_files = input(
            f"{Color.red}MCFM interface source files separated by commas: "
        )
        print("")

        source_files = [sfile.strip() for sfile in source_files.split(",")]

        target_files = []
        for sfile in source_files:
            if ".F90" in sfile:
                tfile = sfile.replace(".F90", ".cpp")
            elif ".h" in sfile:
                tfile = sfile
            else:
                tfile = None
            target_files.append(tfile)

        write_files = [False] * len(target_files)

        instructions = []
        prompt = input(f"{Color.red}USER: ")

        if prompt.upper() == "EXIT":
            break

        for sfile in source_files:
            with open(src_dir + os.sep + sfile, "r") as source:
                # source_code = "".join(source.readlines())
                source_code = source.readlines()

            with open(dest_dir + os.sep + sfile, "w") as dest:

                dest.write(f"LLM-Prompt: {prompt}\n\n")
                chunk_size = 100

                for lines in [
                    source_code[i : i + chunk_size]
                    for i in range(0, len(source_code), chunk_size)
                ]:
                    instructions.append(
                        dict(role="user", content=prompt + ":\n" + "".join(lines))
                    )

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
                        #print(
                        #    f"{Color.blue}{result['generated_text'][-1]['role'].upper()}: "
                        #    + f"{result['generated_text'][-1]['content']}{Color.end}"
                        #)
                        #print("")
                        dest.write(result['generated_text'][-1]['content'])

                    instructions.pop()


if __name__ == "__main__":
    fire.Fire(main)
