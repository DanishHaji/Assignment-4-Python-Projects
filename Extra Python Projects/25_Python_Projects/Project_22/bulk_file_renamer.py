import os
import shutil
from pathlib import Path

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_path(prompt, must_exist=True, allow_files=False):
    """Get a valid filesystem path from user"""
    while True:
        path = input(prompt).strip()
        if not path:
            return None
        
        path = Path(path)
        if not must_exist:
            return path
        
        if not path.exists():
            print(f"Error: Path '{path}' doesn't exist")
            continue
            
        if not allow_files and not path.is_dir():
            print(f"Error: '{path}' is not a folder")
            continue
            
        return path

def list_contents(path, show_files=True, show_folders=True):
    """List files and/or folders at given path"""
    items = []
    for item in path.iterdir():
        if (show_files and item.is_file()) or (show_folders and item.is_dir()):
            items.append(item.name)
    
    print(f"\nFound {len(items)} items:")
    for i, item in enumerate(sorted(items), 1):
        print(f"{i}. {item}")
    return items

def preview_rename(items, prefix="", suffix="", remove="", replace_with=""):
    """Generate rename preview"""
    changes = []
    for item in items:
        name = item.stem
        ext = item.suffix if item.is_file() else ""
        
        # Apply transformations
        if remove:
            name = name.replace(remove, replace_with)
        new_name = f"{prefix}{name}{suffix}{ext}"
        
        changes.append((item.name, new_name))
    
    return changes

def confirm_rename(path, changes):
    """Execute the rename operations"""
    success = 0
    for old, new in changes:
        try:
            old_path = path / old
            new_path = path / new
            
            if old == new:
                continue
                
            if new_path.exists():
                print(f"Skipping '{old}' → '{new}' (already exists)")
                continue
                
            shutil.move(str(old_path), str(new_path))
            success += 1
        except Exception as e:
            print(f"Error renaming '{old}': {e}")
    
    return success

def main():
    clear_screen()
    print("=== Universal Bulk Renamer ===")
    print("Works with any files and folders\n")
    
    
    path = get_valid_path(
        "Enter folder path (or press Enter for current directory): ",
        must_exist=True,
        allow_files=False
    )
    if not path:
        path = Path.cwd()
    
    
    print("\nWhat do you want to rename?")
    print("1. Files only")
    print("2. Folders only")
    print("3. Both files and folders")
    choice = input("Your choice (1-3): ").strip()
    
    show_files = choice in ("1", "3")
    show_folders = choice in ("2", "3")
    
    items = []
    for item in path.iterdir():
        if (show_files and item.is_file()) or (show_folders and item.is_dir()):
            items.append(item)
    
    if not items:
        print("\nNo matching items found!")
        return
    
    
    print("\nSet renaming rules:")
    prefix = input("Add text at start (prefix): ").strip()
    suffix = input("Add text at end (suffix): ").strip()
    remove = input("Text to remove (leave empty to skip): ").strip()
    replace_with = input("Replace with (leave empty to just remove): ").strip() if remove else ""
    
   
    changes = preview_rename(items, prefix, suffix, remove, replace_with)
    print("\nPreview changes:")
    for old, new in changes:
        print(f"{old} → {new}")
    
    
    if input("\nApply these changes? (y/n): ").lower() == 'y':
        success = confirm_rename(path, changes)
        print(f"\nDone! Successfully renamed {success}/{len(changes)} items.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()