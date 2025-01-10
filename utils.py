import os

def write_to_env(file_path: str, key: str, value: str):
    lines = []
    updated = False

    # Check if the file exists, if not create it
    if not os.path.exists(file_path):
        open(file_path, "w").close()

    # Read the existing .env file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Update the key if it exists
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f'{key}="{value}"\n'
            updated = True
            break

    # Add the key if it does not exist
    if not updated:
        lines.append(f'{key}="{value}"\n')

    # Write back to the .env file
    with open(file_path, "w") as file:
        file.writelines(lines)