### Introduction

This is a simple tool to facilitate content management and content development.

The script reports all assets referenced in content JSON files that are missing.

#### Requirements

Modify the script to satisfy your requirements.

At the beginning of the python script, specify:
1. The folder(s) that contain the assets
2. The folder(s) that contain the content JSON
3. The relevant JSON file(s), **only** if any content JSON is not embedded in a folder

The `check_assets()` function expects two arguments: 
1. The category name (e.g. "images")
2. The extension (e.g. "png")

For instance, the example output below requires three calls of the function:

```
check_assets(asset_label="images", asset_extension="png")
check_assets(asset_label="sound files", asset_extension="mp3")
check_assets(asset_label="videos", asset_extension="mp4")
```

#### Example output

Output generated when running `python main.py` for the files included in this repo.

![image](https://github.com/user-attachments/assets/b0d9c671-0d30-40b6-942c-b9449509b666)
