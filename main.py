import os
import re
from pathlib import Path

# USER: specify assets folder(s)
#       assets_folders is a list containing one or more dictionaries.
#       Each dictionary represents a folder with assets:
#           the "filename" key specifies the directory path
#           the "recursive" key indicates whether to include assets in nested subdirectories
#           within the specified folder.
assets_folders = [
    {
        "filename": "assets/",
        "recursive": True
    }
]

# USER: specify JSON folder(s)
#       json_folders is a list containing one or more dictionaries.
#       Each dictionary represents a folder with JSON files:
#           the "filename" key specifies the directory path
#           the "recursive" key indicates whether to include JSON files in nested subdirectories
#           within the specified folder.
#       If there are no relevant JSON folders, use an empty list: json_folders = []
json_folders = [
    {
        "filename": "json/",
        "recursive": True
    }
]


# NOTE:
# for detecting asset filenames in the JSON, the script requires that your
# assets filenames include an extension that starts with a period,
# for instance ".png" for an image filename


def main():
    json_files = []
    # Add all JSON files from relevant JSON folders, if any
    for folder in json_folders:
        if not os.path.isdir(folder["filename"]):
            print(f"ERROR: unable to find folder '{folder["filename"]}'")
            return

    try:
        json_files.extend(
            [
                str(filename)
                for folder in json_folders
                for filename in (Path(folder["filename"]).rglob("*.json") if folder["recursive"] else Path(folder["filename"]).glob("*.json"))
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
        if not os.path.isdir(folder["filename"]):
            print(f"ERROR: unable to find folder '{folder}'")
            return

    # Check assets, specifying an output label and a file extension
    check_assets(json_files, asset_label="images", asset_extension="png")
    check_assets(json_files, asset_label="sound files", asset_extension="mp3")
    check_assets(json_files, asset_label="videos", asset_extension="mp4")


def check_assets(json_files, asset_label="soundfiles", asset_extension="mp3"):
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
            filename for filename in Path(folder["filename"]).rglob(f"*.{asset_extension}")
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
