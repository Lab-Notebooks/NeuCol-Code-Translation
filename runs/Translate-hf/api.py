# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

from types import SimpleNamespace

colors = SimpleNamespace(
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


def get_user_input(input_text):
    user_input = input(f"\n{colors.darkcyan}{input_text}: {colors.end}")
    return user_input


def display_output(output_text):
    print(f"{colors.red}{output_text}{colors.end}")
