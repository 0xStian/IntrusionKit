import subprocess
import sys
import os
import shutil


output_directory = "ReverseShell_Output"
script_name = "hello_world.py"
exe_name = "hello_world"

script_content = '''print("Hello, World!")
x=input()'''


with open(script_name, "w") as file:
    file.write(script_content)


try:
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    subprocess.check_call([
        sys.executable, '-m', 'PyInstaller',
        '--onefile',  # single executable
        '--noconfirm',  # Overwrite existing files
        '--distpath', output_directory,  # output directory
        script_name  # Name
    ])
    
    # Cleanup
    build_dir = "build"
    spec_file = f"{exe_name}.spec"
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(spec_file):
        os.remove(spec_file)

    print(f"Executable created successfully in {output_directory}.")
    
except subprocess.CalledProcessError as e:
    print(f"Failed to create executable: {e}")

