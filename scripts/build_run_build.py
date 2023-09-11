import subprocess

# Define the build command as a list of arguments
build_command = ["dir *.*"]  # "python -m build"]  # , "arg1", "arg2", ...]

try:
    # Run the build command
    process = subprocess.Popen(build_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True)

    # Capture and print the command's standard output and standard error
    stdout, stderr = process.communicate()
    print("Standard Output:")
    print(stdout)
    print("Standard Error:")
    print(stderr)

    # Check the return code to determine if the command was successful
    return_code = process.returncode
    if return_code == 0:
        print("Build successful")
    else:
        print(f"Build failed with return code {return_code}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
