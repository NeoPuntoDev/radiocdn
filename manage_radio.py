import argparse
import json
import os
import re
from PIL import Image

JSON_FILE = "stream.json"
IMG_DIR = "img"
CDN_PREFIX = "https://cdn.jsdelivr.net/gh/MXNeoPunto/radiocdn@main/img/"

def create_slug(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def load_data():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")

def reorder_ids(radios):
    # IMPORTANT: DO NOT MODIFY THIS FUNCTION LOGIC
    # It recalculates IDs sequentially starting from 1 for all items in the array.
    # This automatically fills any gaps when an item is deleted (e.g. 1,2,4 becomes 1,2,3).
    # It also ensures new items get the next sequential number automatically (e.g. 1,2,3 becomes 1,2,3,4).
    for index, radio in enumerate(radios):
        radio["id"] = index + 1
    return radios

def add_radio(args):
    data = load_data()
    radios = data.get("radios", [])

    slug = create_slug(args.name)
    img_filename = f"{slug}.webp"
    img_path = os.path.join(IMG_DIR, img_filename)

    # Process image
    try:
        with Image.open(args.image) as img:
            img.save(img_path, "WEBP", quality=85)
            print(f"Image saved as {img_path}")
    except Exception as e:
        print(f"Error processing image {args.image}: {e}")
        return

    # Remove original image if it's in the root
    if os.path.exists(args.image) and os.path.dirname(args.image) == "":
        os.remove(args.image)
        print(f"Removed original image {args.image}")

    cdn_url = f"{CDN_PREFIX}{img_filename}"

    # Check if radio exists and update or add new
    existing = next((r for r in radios if r["name"].lower() == args.name.lower()), None)

    new_radio = {
        "id": 0, # Will be automatically calculated by reorder_ids() below
        "name": args.name,
        "image": cdn_url,
        "stream_url": args.url,
        "description": args.desc if args.desc else "Alabanza y adoración",
        "popular": False,
        "language": args.lang
    }

    if existing:
        print(f"Updating existing radio: {args.name}")
        existing.update(new_radio)
    else:
        print(f"Adding new radio: {args.name}")
        radios.append(new_radio)

    data["radios"] = reorder_ids(radios)
    save_data(data)
    print("Radio successfully added and IDs reordered.")

def delete_radio(args):
    data = load_data()
    radios = data.get("radios", [])

    if args.id:
        target_radio = next((r for r in radios if r["id"] == args.id), None)
    elif args.name:
        target_radio = next((r for r in radios if r["name"].lower() == args.name.lower()), None)
    else:
        print("Please provide --id or --name to delete.")
        return

    if not target_radio:
        print("Radio not found.")
        return

    radios.remove(target_radio)

    # Attempt to delete the image file
    img_url = target_radio.get("image", "")
    if CDN_PREFIX in img_url:
        img_filename = img_url.replace(CDN_PREFIX, "")
        img_path = os.path.join(IMG_DIR, img_filename)
        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"Removed image {img_path}")

    data["radios"] = reorder_ids(radios)
    save_data(data)
    print(f"Radio '{target_radio['name']}' successfully deleted and IDs reordered.")

def main():
    parser = argparse.ArgumentParser(description="Manage radio station directory.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new radio station.")
    add_parser.add_argument("--name", required=True, help="Name of the radio station.")
    add_parser.add_argument("--url", required=True, help="Stream URL.")
    add_parser.add_argument("--image", required=True, help="Path to the original image file in the root directory.")
    add_parser.add_argument("--desc", help="Description of the radio (optional).")
    add_parser.add_argument("--lang", help="Language of the radio (es, en). Default is es.", default="es")

    delete_parser = subparsers.add_parser("delete", help="Delete a radio station.")
    delete_group = delete_parser.add_mutually_exclusive_group(required=True)
    delete_group.add_argument("--id", type=int, help="ID of the radio station to delete.")
    delete_group.add_argument("--name", help="Name of the radio station to delete.")

    args = parser.parse_args()

    if args.action == "add":
        add_radio(args)
    elif args.action == "delete":
        delete_radio(args)

if __name__ == "__main__":
    main()
