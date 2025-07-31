import os
import sys

# This script generates CMakeLists.txt files for a given directory and its subdirectories.
# This is useful for copying old projects into a new directory structure

# target_include_directories(target_name PUBLIC
# 	"${CMAKE_CURRENT_SOURCE_DIR}"
# )
#
# target_sources(target_name PRIVATE
# 	"${CMAKE_CURRENT_SOURCE_DIR}/src.cpp"
# 	"${CMAKE_CURRENT_SOURCE_DIR}/src.h"
# )
#
# add_subdirectory(dir1)
# add_subdirectory(dir2)



def generate_cmakelists(directory, target_name="renderlib"):
    """Generates CMakeLists.txt for a given directory and its subdirectories."""

    cmake_content = ""
    cmake_content += f"target_include_directories({target_name} PUBLIC \"${{CMAKE_CURRENT_SOURCE_DIR}}\")\n\n"

    source_files = []
    subdirectories = []

    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item.endswith((".cpp", ".c", ".cc", ".h", ".hpp")):
            source_files.append(item)
        elif os.path.isdir(item_path):
            subdirectories.append(item)

    # If there are source files, add them to the target
    if not source_files and not subdirectories:
        print(f"Warning: No source files found in {directory}. Skipping CMakeLists.txt generation.")
        return

    if source_files:
        cmake_content += f"target_sources({target_name} PRIVATE\n"
        for source_file in source_files:
            cmake_content += f"    \"${{CMAKE_CURRENT_SOURCE_DIR}}/{source_file}\"\n"
        cmake_content += ")\n\n"

    if subdirectories:
        for subdirectory in subdirectories:
            cmake_content += f"add_subdirectory({subdirectory})\n"

    with open(os.path.join(directory, "CMakeLists.txt"), "w") as f:
        f.write(cmake_content)

    for subdirectory in subdirectories:
        generate_cmakelists(os.path.join(directory, subdirectory), target_name)

if __name__ == "__main__":
    target_directory = "."  # Current directory as default
    cmake_target_name = "renderlib"  # Default target name
    if len(sys.argv) > 1:
        target_directory = sys.argv[1]
    if len(sys.argv) > 2:
        cmake_target_name = sys.argv[2]
    generate_cmakelists(target_directory, cmake_target_name)
    print("CMakeLists.txt files generated.")