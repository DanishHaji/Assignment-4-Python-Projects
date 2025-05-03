import os
import shutil
import streamlit as st
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Smart File/Folder Renamer",
    page_icon="🛠️",
    layout="wide"
)

# Header
st.title("🛠️ Smart File/Folder Renamer")
st.write("Easily preview and rename files or folders in a given directory using simple replace rules.")

# Input section
st.subheader("📁 Directory Selection")
directory_input = st.text_input("Enter directory path:", value="")
path = Path(directory_input)

# Preview type
view_option = st.radio("Preview:", ["Files", "Folders"], horizontal=True)

# Function to list items based on selection
def list_items(path: Path, option: str):
    if not path.exists():
        return []
    if option == "Files":
        return [f for f in path.iterdir() if f.is_file()]
    elif option == "Folders":
        return [f for f in path.iterdir() if f.is_dir()]
    else:
        return list(path.iterdir())

# Preview items
if st.button("🔍 Preview"):
    if not path.exists():
        st.error("Invalid path! Please enter a correct directory path.")
    else:
        items = list_items(path, view_option)
        if not items:
            st.warning("No items found.")
        else:
            item_names = [item.name for item in items]
            st.success(f"Found {len(item_names)} items.")
            st.dataframe(pd.DataFrame({"Name": item_names}), use_container_width=True)
            st.session_state["items"] = items  # Store items for renaming

# Renaming rules
st.subheader("✂️ Renaming Rules")
text_to_remove = st.text_input("Text to remove:")
text_to_replace = st.text_input("Replace with:")

# Rename button
if "items" in st.session_state and st.button("✅ Rename Items"):
    items = st.session_state["items"]
    success, skipped, errors = 0, 0, 0
    renamed_data = []

    for item in items:
        original = item.name
        new_name = original.replace(text_to_remove, text_to_replace)
        new_path = item.parent / new_name

        if original == new_name or new_path.exists():
            skipped += 1
            continue

        try:
            shutil.move(str(item), str(new_path))
            success += 1
            renamed_data.append({"Old Name": original, "New Name": new_name, "Status": "Renamed"})
        except Exception as e:
            errors += 1
            renamed_data.append({"Old Name": original, "New Name": new_name, "Status": f"Error: {e}"})

    st.success(f"Renaming complete ✅\n- Renamed: {success}\n- Skipped: {skipped}\n- Errors: {errors}")

    if renamed_data:
        st.dataframe(pd.DataFrame(renamed_data), use_container_width=True)