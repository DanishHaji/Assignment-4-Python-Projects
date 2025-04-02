import os
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
from mimetypes import guess_extension
from tkinter import Tk, Label, Entry, Button, messagebox, filedialog
from typing import List, Tuple, Dict, Any

def get_github_avatar(username: str) -> str:
    """Fetches the GitHub profile avatar URL for a given username."""
    url = f"https://github.com/{username}"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Selectors to match avatar
        selectors: List[Tuple[str, Dict[str, str]]] = [
            ('div', {'class': 'avatar avatar-user'}),  # Current GitHub layout
            ('img', {'alt': 'Avatar'}),               # Old layout
            ('img', {'class': 'avatar'})              # Alternative
        ]

        for tag, attrs in selectors:
            element = soup.find(tag, attrs=attrs)
            if isinstance(element, Tag):
                src = element.get("src")
                if src:
                    return str(src).split("?")[0]  # Remove URL parameters

        return "Error: Profile image not found."

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def download_avatar(url: str, save_dir: str = "avatars") -> str:
    """Downloads the GitHub avatar from a given URL and saves it with the correct file extension."""
    try:
        if not url.startswith(('http://', 'https://')):
            return "❌ Invalid URL for avatar image."

        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)

        # Get the content type and determine the file extension
        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        file_extension = guess_extension(content_type.split(";")[0]) or ".png"

        # Generate a filename with the correct extension
        filename = os.path.basename(urlparse(url).path)
        if not filename.endswith(('.jpg', '.png', '.jpeg')):
            filename += file_extension

        save_path = os.path.join(save_dir, filename)

        # Save the image
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return f"✅ Image saved as '{save_path}'"
    except Exception as e:
        return f"❌ Download failed: {str(e)}"

def cli_interface():
    """Command-line interface to fetch and download GitHub avatars."""
    print("GitHub Profile Image Scraper")
    print("----------------------------")

    while True:
        username = input("\nEnter GitHub username (or 'q' to quit): ").strip()
        if username.lower() == 'q':
            break

        if not username:
            print("⚠️ Please enter a valid username.")
            continue

        print("\n⌛ Fetching profile...")
        avatar_url = get_github_avatar(username)

        print("\n🔍 Result:")
        print(avatar_url)

        if avatar_url.startswith(('http://', 'https://')):
            choice = input("\nDownload image? (y/n): ").lower()
            if choice == 'y':
                custom_dir = input(f"Save to directory [default: 'avatars']: ").strip()
                save_dir = custom_dir if custom_dir else "avatars"
                print(download_avatar(avatar_url, save_dir))

        print("-" * 50)

def gui_interface():
    """Graphical user interface to fetch and download GitHub avatars."""
    def on_submit():
        username = entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter a username.")
            return

        avatar_url = get_github_avatar(username)

        if avatar_url.startswith(('http://', 'https://')):
            save_path = filedialog.askdirectory(title="Select Save Location")

            if not save_path:
                messagebox.showwarning("Warning", "No directory selected. Image not downloaded.")
                return

            result = download_avatar(avatar_url, save_path)
            messagebox.showinfo("Success", f"{result}\n\nURL: {avatar_url}")
        else:
            messagebox.showerror("Error", avatar_url)

    root = Tk()
    root.title("GitHub Avatar Scraper")
    root.geometry("400x200")

    Label(root, text="GitHub Username:", font=("Arial", 12)).pack(pady=10)
    entry = Entry(root, font=("Arial", 12))
    entry.pack(pady=5)
    Button(root, text="Get & Download Avatar", command=on_submit, bg="#4CAF50", fg="white").pack(pady=15)
    Button(root, text="Exit", command=root.destroy, bg="#f44336", fg="white").pack()

    root.mainloop()

if __name__ == "__main__":
    print("Choose interface mode:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")

    while True:
        choice = input("Enter choice (1/2): ").strip()
        if choice == "1":
            cli_interface()
            break
        elif choice == "2":
            gui_interface()
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
