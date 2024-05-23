# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

# Import libraries
from typing import Optional
import fire
import transformers
import torch
import json
from types import SimpleNamespace
import os

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
    max_new_tokens: int = 2048,
    batch_size: int = 8,
    max_length: Optional[int] = None,
):

    choice = input(
        f"{Color.darkcyan}Welcome to a simple AI powered chat that uses the transformers API "+
        f"to test different models.\n\t1. mistral-7b\n\t2. codellama-7b\n\t3. gemma-7b\nSelect "+
        f"the model you would like to interact with: "
    )

    print(f"{Color.end}")

    if int(choice) == 1:
        ckpt_dir = os.getenv("MODEL_HOME") + os.sep + "mistral/Mistral-7B-Instruct-v0.1"
    elif int(choice) == 2:
        ckpt_dir = (
            os.getenv("MODEL_HOME") + os.sep + "codellama/CodeLlama-7b-Instruct-hf"
        )
    elif int(choice) == 3:
        ckpt_dir = (
            os.getenv("MODEL_HOME") + os.sep + "google/gemma-7b-it"
        )    
    else:
        raise ValueError(f"Option {choice} not defined")

    tokenizer = transformers.AutoTokenizer.from_pretrained(ckpt_dir)

    pipeline = transformers.pipeline(
        "text-generation",
        model=ckpt_dir,
        torch_dtype=torch.float16,
        device=0,
    )

    chat_name = input(f"{Color.darkcyan}Enter chat transcript name: ")
    print("")

    instructions = []

    while True:
        prompt = input(f"{Color.red}USER: ")

        if prompt.upper() == "EXIT":
            break

        instructions.append(dict(role="user", content=prompt))

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
            print(
                f"{Color.blue}{result['generated_text'][-1]['role'].upper()}: "+
                f"{result['generated_text'][-1]['content']}{Color.end}"
            )
            print("")
            instructions.append(result["generated_text"][-1])

    with open(f"{chat_name}.json", "w") as outfile:
        json.dump(
            {
                "configuration": dict(
                    ckpt_dir=ckpt_dir,
                    max_new_tokens=max_new_tokens,
                    max_length=max_length,
                    batch_size=batch_size,
                ),
                "chat": instructions,
            },
            outfile,
            indent=2,
        )


if __name__ == "__main__":
    fire.Fire(main)
