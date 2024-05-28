# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

# Import libraries
import os, sys

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api, neucol

from typing import Optional
import fire, transformers, torch


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
        raise ValueError(f"Option {llm_choice} not defined")

    dest = api.get_user_input('Enter destination folder name (prefix it with "src_")')
    mapping = neucol.create_src_mapping(dest)

    source_dirs = api.get_user_input(
        "MCFM interface src directories separated by commas, use (*) for all"
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
        raise ValueError(
            "source_files and target_files for conversion do not match in length"
        )

    instructions = []
    prompt = api.get_user_input("LLM-Prompt")

    tokenizer = transformers.AutoTokenizer.from_pretrained(ckpt_dir)

    pipeline = transformers.pipeline(
        "text-generation",
        model=ckpt_dir,
        torch_dtype=torch.float16,
        device=0,
    )

    for sfile, tfile in zip(source_files, target_files):

        with open(sfile, "r") as source:
            source_code = source.readlines()

        with open(tfile, "w") as destination:
            destination.write(f"# LLM-Prompt: {prompt}\n\n")
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
                    destination.write(result["generated_text"][-1]["content"])

                instructions.pop()


if __name__ == "__main__":
    fire.Fire(main)
