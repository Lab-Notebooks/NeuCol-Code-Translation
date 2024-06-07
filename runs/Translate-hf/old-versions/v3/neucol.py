# Module for build managing directory tree

import os, sys, glob

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api


def infer_src_mapping(sfile, mapping):
    prompt = []
    return prompt


def create_src_mapping(dest):
    """
    Build directory tree from neucol source code.

    Arguments
    ---------
    dest : String value of destination directory
    """
    src_dir = os.getenv("MCFM_HOME") + os.sep + "src"
    dest_dir = os.getenv("MCFM_HOME") + os.sep + dest

    if os.path.exists(dest_dir):
        user_decision = api.get_user_input(
            f'Destination "{dest}" already exists continue? (Y/n)'
        )
        if user_decision.upper() == "Y":
            api.display_output(
                "Please note that existing files will not be replaced in the destination."
            )
        elif user_decision.upper() == "N":
            api.display_output("Exiting application based on user decision")
        else:
            api.display_output(f'Unknown option "{user_option}"')
            raise ValueError

    else:
        api.display_output(f'Creating desitnation directory "{dest}"')
        for item in os.walk(src_dir):
            sub_dir = item[0].replace(src_dir, "")
            os.makedirs(dest_dir + os.sep + sub_dir)

    src_files = []
    dest_files = []

    for item in os.walk(src_dir):

        sub_dir = item[0].replace(src_dir, "")

        for file in item[2]:
            src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
            dest_files.append(dest_dir + os.sep + sub_dir + os.sep + file)

    mapping = {
        "src": {"files": src_files, "dir": src_dir},
        "dest": {"files": dest_files, "dir": dest_dir},
    }

    return mapping
