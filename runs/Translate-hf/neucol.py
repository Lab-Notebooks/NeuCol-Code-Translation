# Module for build managing directory tree

import os, sys, glob

for path in os.getenv("PYMODULE_PATH").split(":"):
    sys.path.insert(0, path)

import api


def infer_src_mapping(sfile, mapping):

    prompt = []

    if sfile == mapping["src"]["dir"] + os.sep + "Mods/AllModules.h":
        prompt.append(
            "Convert this file to a C++ header file. Note that inputs are chunks which belong to same file, do not try "
            + "to infer around the input or provide any context. Simply convert the source code from FORTRAN to C++."
        )
    else:
        prompt.append(
            "Convert this file to a C++ source code file. Note that inputs are chunks which belong to same file, do not try "
            + "to infer around the input or provide any context. Simply convert the source code from FORTRAN to C++."
        )
        prompt.append(
            "The code blocks you will receive are part of a bigger codebase so do not add "
            + "additional function declarations, or a main function definition. Just do the conversion process line-by-line."
        )

        prompt.append(
            'Replace "use" statements in FORTRAN with "#include "Mods/AllModules.h" in the C++ version.'
        )
        prompt.append(
            'Put the "#include" statement at the top of the file and assume that any '
            + "variables that are not declared in the file are available in the header file."
        )

    prompt.append('Treat "real(dp)" as "real(*8)", and "complex(dp)" as "complex(*8)".')

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
            sub_dir = item[0].replace(src_dir + os.sep, "")
            os.makedirs(dest_dir + os.sep + sub_dir)

    src_files = []
    dest_files = []

    for item in os.walk(src_dir):

        sub_dir = item[0].replace(src_dir + os.sep, "")

        for file in item[2]:
            if not file.endswith(
                ("_mod.f", "_mod.f90", ".cxx", ".lh", ".sh", ".txt", "README", ".h")
            ) and not file.startswith("mod_"):
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
