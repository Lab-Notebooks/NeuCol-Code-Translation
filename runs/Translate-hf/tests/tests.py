# Prompt engineering for building diffusion stencils for constant and variable coefficient equation

import os, sys

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api, neucol

def main():
    dest = api.get_user_input('Enter destination folder name (prefix it with "src_")')
    mapping = neucol.create_src_mapping(dest)

    for src_file, dest_file in zip(mapping["src"]["files"], mapping["dest"]["files"]):
        if "AllModules.h" in src_file:
            api.display_output(f"Test Output:\n{src_file}, {dest_file}")


if __name__ == "__main__":
    main()
