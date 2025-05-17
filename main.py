import os
import re
from pathlib import Path

# NOTE:
# for detecting asset filenames in the JSON, the script requires that your
# assets filenames include an extension that starts with a period,
# for instance ".png" for an image filename


def check_assets(asset_label="soundfiles", asset_extension="mp3"):
    """Checks to see if all assets included in JSON are present in a folder with assets"""
    # arguments:
    #   asset_label is the output label for the category of asset checked
    #   asset_extension is the filename extension associated with the asset
    asset_extension = asset_extension.lstrip(".")
    json_assets = []

    # Create list of all relevant asset filenames in JSON files
    for json_file in json_files:
        with open(json_file, "r") as filename:
            json_text = filename.read()
            json_assets.extend(re.findall(rf"[^\"]*\.{asset_extension}", json_text))
    json_assets = set(json_assets)

    # Create list of relevant assets in assets folder(s)
    assets_files = []
    for folder in assets_folders:
        assets_files.extend(
            filename for filename in Path(folder).rglob(f"*.{asset_extension}")
        )
    assets_files = set(map(os.path.basename, assets_files))

    # Check to see if any assets are missing
    missing_assets = json_assets - assets_files

    if missing_assets:
        # Report missing assets
        print(
            f"\n\033[41m{len(missing_assets)} MISSING {asset_label.upper()}\033[0m (.{asset_extension})"
        )
        for asset in missing_assets:
            print(asset)
    else:
        # Report no assets are missing
        print(
            f"\n\033[0;42mNO MISSING {asset_label.upper()}\033[0m (.{asset_extension})"
        )


def main():
    # Add all JSON files from relevant JSON folders, if any
    for folder in json_folders:
        if not os.path.isdir(folder):
            print(f"ERROR: unable to find folder '{folder}'")
            return

    try:
        json_files.extend(
            [
                str(filename)
                for folder in json_folders
                for filename in Path(folder).rglob("*.json")
            ]
        )
    except:
        pass

    try:
        json_files
    except:
        print("ERROR: Please specify one or more valid JSON files and/or JSON folders")
        return

    for filename in json_files:
        if not os.path.isfile(filename):
            print(f"ERROR: Unable to find file '{filename}'")
            return

    try:
        assets_folders
    except:
        print("ERROR: Please specify one or more existing assets folders")
        return

    for folder in assets_folders:
        if not os.path.isdir(folder):
            print(f"ERROR: unable to find folder '{folder}'")
            return

    # Check assets, specifying an output label and a file extension
    check_assets(asset_label="images", asset_extension="png")
    check_assets(asset_label="soundfiles", asset_extension="mp3")
    check_assets(asset_label="videos", asset_extension="mp4")


if __name__ == "__main__":

    # USER: specify assets folder
    assets_folders = ["assets/"]

    # USER: specify all relevant folders that include JSON files
    #   if there are no relevant JSON folders, use empty list: json_folders = []
    json_folders = []

    # USER: specify all relevant individual JSON files
    #  if there are no relevant individual JSON files, use empty list: json_files = []
    json_files = ["items.json"]

    main()
