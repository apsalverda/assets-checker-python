import os
import re
from pathlib import Path

# USER: below, specify assets_folders, json_folders, and assets_to_check according to your needs

# USER: specify assets folder(s)
#       assets_folders is a list containing one or more dictionaries.
#       Each dictionary represents a folder with assets:
#           the "path" key (str) specifies the directory path
#           the "recursive" key (bool) indicates whether to include assets in nested subdirectories
#           within the specified folder.
assets_folders = [
    {
        "path": "assets/",
        "recursive": True
    }
]

# USER: specify JSON folder(s)
#       json_folders is a list containing one or more dictionaries.
#       Each dictionary represents a folder with JSON files:
#           the "path" key (str) specifies the directory path
#           the "recursive" (bool) key indicates whether to include JSON files in nested subdirectories
#           within the specified folder.
#       If there are no relevant JSON folders, use an empty list: json_folders = []
json_folders = [
    {
        "path": "json/",
        "recursive": True
    }
]

# USER: specify assets to check
#       assets_to_check is a list containing one or more dictionaries.
#       Each dictionary represents an asset:
#           the "asset_label" key (str) specifies the label used in the output
#           the "asset_extension" key (str) specifies the extension that defines the asset
# NOTE:
# for detecting asset filenames in the JSON, the script requires that your
# assets filenames include an extension that starts with a period,
# for instance ".png" for an image filename

assets_to_check = [
    {"asset_label": "images", "asset_extension": "png"},
    {"asset_label": "sound files", "asset_extension": "mp3"},
    {"asset_label": "videos", "asset_extension": "mp4"}
]


def main():
    json_files = []
    # Add all JSON files from relevant JSON folders
    for folder in json_folders:
        if not os.path.isdir(folder["path"]):
            print(f"ERROR: unable to find folder '{folder["path"]}'")
            return

    try:
        json_files.extend(
            [
                str(filename)
                for folder in json_folders
                for filename in (Path(folder["path"]).rglob("*.json") if folder["recursive"] else Path(folder["path"]).glob("*.json"))
            ]
        )

    except NameError:
        pass

    try:
        json_files
    except NameError:
        print("ERROR: Please specify one or more valid JSON folders")
        return

    try:
        assets_folders
    except NameError:
        print("ERROR: Please specify one or more existing assets folders")
        return

    for folder in assets_folders:
        if not os.path.isdir(folder["path"]):
            print(f"ERROR: unable to find folder '{folder}'")
            return

    # Check assets
    for asset in assets_to_check:
        check_assets(json_files, asset["asset_label"], asset["asset_extension"])

def check_assets(json_files, asset_label, asset_extension):
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
    assets_files.extend(
        [
            str(path)
            for folder in assets_folders
            for path in (
            Path(folder["path"]).rglob(f"*.{asset_extension}") if folder["recursive"] else Path(folder["path"]).glob(f"*.{asset_extension}")
        )
        ]
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


if __name__ == "__main__":

    main()
