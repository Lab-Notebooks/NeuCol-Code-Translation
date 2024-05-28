# Module for build managing directory tree

import os, sys, glob

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)


def infer_src_mapping(mapping):
    pass


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
        raise ValueError(f"Cannot create {dest_dir}. Already Exists.")

    src_files = []
    dest_files = []

    for item in os.walk(src_dir):

        sub_dir = item[0].replace(src_dir + os.sep, "")
        os.makedirs(dest_dir + os.sep + sub_dir)

        for file in item[2]:
            if not file.endswith(
                ("_mod.f90", ".cxx", ".lh", ".sh", ".txt", "README", ".h")
            ):
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)

                if file.endswith((".F90", ".f", ".f90")):
                    dest_files.append(
                        dest_dir
                        + os.sep
                        + sub_dir
                        + os.sep
                        + file.replace(".F90", ".cxx")
                        .replace(".f", ".cxx")
                        .replace(".f90", ".cxx")
                    )

                else:
                    raise ValueError(f"Unrecognized extension for file: {file}")

            if file.endswith("AllModules.h"):
                src_files.append(src_dir + os.sep + sub_dir + os.sep + file)
                dest_files.append(dest_dir + os.sep + sub_dir + os.sep + file)

    mapping = {
        "src": {"files": src_files, "dir": src_dir},
        "dest": {"files": dest_files, "dir": dest_dir},
    }

    return mapping
