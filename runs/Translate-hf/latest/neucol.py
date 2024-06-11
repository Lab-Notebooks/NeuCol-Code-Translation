# Module for build managing directory tree

import os, sys, glob, toml

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api


def infer_src_mapping(sfile, mapping):
    prompt = []
    return prompt


def create_src_mapping(filemap):
    """
    Build directory tree from neucol source code.

    Arguments
    ---------
    dest : String value of destination directory
    """
    src_dir = os.getenv("MCFM_HOME") + os.sep + "src"
    dest_dir = os.getenv("MCFM_HOME") + os.sep + "src"

    input_files = toml.load(filemap)

    src_files = []
    dest_files = []

    api.display_output(f'Mapping files from "{filemap}"')
    api.display_output(
        "Please note that existing files will not be replaced in the destination."
    )

    for item in os.walk(src_dir):

        sub_dir = item[0].replace(src_dir, "")

        for file in item[2]:
            if sub_dir + os.sep + file in input_files["sources"]:
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
                if file.endswith(".f"):
                    dest_files.append(
                        dest_dir
                        + os.sep
                        + sub_dir
                        + os.sep
                        + file.replace(".f", ".cpp")
                    )

                elif file.endswith(".cpp"):
                    dest_files.append(
                        dest_dir
                        + os.sep
                        + sub_dir
                        + os.sep
                        + file.replace(".cpp", ".f90")
                    )
                else:
                    api.display_output(
                        f"source {sub_dir + os.sep + file} not recognized."
                    )
                    raise NotImplementedError

            elif sub_dir + os.sep + file in input_files["headers"]:
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
                if file.endswith(".f90"):
                    dest_files.append(
                        dest_dir
                        + os.sep
                        + sub_dir
                        + os.sep
                        + file.replace(".f90", ".hpp")
                    )
                elif file.endswith(".hpp"):
                    dest_files.append(
                        dest_dir
                        + os.sep
                        + sub_dir
                        + os.sep
                        + file.replace(".hpp", ".f90")
                    )
                else:
                    api.display_output(
                        f"header {sub_dir + os.sep + file} not recognized."
                    )
                    raise NotImplementedError

    mapping = {
        "src": {"files": src_files, "dir": src_dir},
        "dest": {"files": dest_files, "dir": dest_dir},
    }

    return mapping
