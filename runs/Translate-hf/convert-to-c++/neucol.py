# Module for build managing directory tree

import os, sys, glob, toml

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api


def infer_src_mapping(sfile, mapping):
    prompt = []
    return prompt


def create_src_mapping(file_map):
    """
    Build directory tree from neucol source code.

    Arguments
    ---------
    dest : String value of destination directory
    """
    src_dir = os.getenv("MCFM_HOME") + os.sep + "src"
    dest_dir = os.getenv("MCFM_HOME") + os.sep + "src"

    input_files = toml.load(file_map)

    src_files = []
    dest_files = []

    api.display_output(f'Mapping files from "{file_map}"')
    api.display_output(
        "Please note that existing files will not be replaced in the destination."
    )

    for item in os.walk(src_dir):

        sub_dir = item[0].replace(src_dir, "")

        for file in item[2]:
            if sub_dir + os.sep + file in input_files["sources"]:
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
                dest_files.append(
                    dest_dir + os.sep + sub_dir + os.sep + file.replace(".f", ".cpp")
                )

            elif sub_dir + os.sep + file in input_files["headers"]:
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
                dest_files.append(
                    dest_dir + os.sep + sub_dir + os.sep + file.replace(".f90", ".hpp")
                )

    mapping = {
        "src": {"files": src_files, "dir": src_dir},
        "dest": {"files": dest_files, "dir": dest_dir},
    }

    return mapping
