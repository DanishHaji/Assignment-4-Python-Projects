import os
from typing import List

def get_files_in_directory(folder_path: str, file_extension: str = "") -> List[str]:
    """
    Retrieves the list of files in the specified directory.
    Filters files by extension if provided.
    """
    try:
        files = [
            file for file in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, file))
        ]
        if file_extension:
            files = [file for file in files if file.endswith(file_extension)]
        return files
    except FileNotFoundError:
        print(f"❌ Error: Folder '{folder_path}' not found.")
        return []
    except PermissionError:
        print(f"❌ Error: Permission denied to access '{folder_path}'.")
        return []

def rename_files(folder_path: str, files: List[str], prefix: str = "", suffix: str = "", replace_text: str = "") -> None:
    """
    Renames files based on user-defined conditions such as prefix, suffix, or text replacement.
    """
    for index, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        file_name, file_ext = os.path.splitext(file)

        # Apply text replacement if specified
        if replace_text:
            file_name = file_name.replace(replace_text, "")

        # Generate new filename
        new_name = f"{prefix}{file_name}{suffix}{file_ext}"
        new_file_path = os.path.join(folder_path, new_name)

        # Rename file
        try:
            os.rename(file_path, new_file_path)
            print(f"✅ Renamed: '{file}' -> '{new_name}'")
        except Exception as e:
            print(f"❌ Failed to rename '{file}': {str(e)}")

def bulk_file_renamer():
    """
    Main function to execute the Bulk File Re-namer program.
    """
    print("Bulk File Re-namer")
    print("-------------------")

    # Step 1: Get folder path
    folder_path = input("Enter the folder path: ").strip()
    if not os.path.exists(folder_path):
        print("⚠️ Error: Specified folder does not exist.")
        return

    # Step 2: Filter files by extension
    file_extension = input("Enter the file extension to target (e.g., '.txt') or leave blank for all files: ").strip()
    files = get_files_in_directory(folder_path, file_extension)
    if not files:
        print("⚠️ No files found in the specified folder.")
        return

    # Step 3: Rename conditions
    print("\nRename Conditions:")
    prefix = input("Enter prefix for filenames (optional): ").strip()
    suffix = input("Enter suffix for filenames (optional): ").strip()
    replace_text = input("Enter text to replace/remove in filenames (optional): ").strip()
    replace_text = replace_text or ""  # Avoid None type errors
    print("\nPreview of changes:")
    
    # Preview changes
    for index, file in enumerate(files):
        file_name, file_ext = os.path.splitext(file)
        new_name = f"{prefix}{file_name.replace(replace_text, '')}{suffix}{file_ext}" if replace_text else f"{prefix}{file_name}{suffix}{file_ext}"
        print(f"{index + 1}. {file} -> {new_name}")

    # Step 4: Confirmation
    confirm = input("\nDo you want to apply these changes? (y/n): ").strip().lower()
    if confirm == "y":
        rename_files(folder_path, files, prefix, suffix, replace_text)
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    bulk_file_renamer()
