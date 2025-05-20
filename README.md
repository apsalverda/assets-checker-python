### Introduction

This is a simple tool that identifies missing assets (such as image, audio and video files) referenced in content JSON.

#### Example output

Output generated when running `python main.py` for the files included in this repo.

![image](https://github.com/user-attachments/assets/b0d9c671-0d30-40b6-942c-b9449509b666)

#### Usage

Modify the Python script according to your requirements.

At the top of the script, specify:
1. The folder(s) that contain the assets
2. The folder(s) that contain the content JSON
3. The relevant assets to check (category label, file extension), for instance:
```
assets_to_check = [
  {"asset_label": "images", "asset_extension": "png"},
  {"asset_label": "sound files", "asset_extension": "mp3"},
  {"asset_label": "videos", "asset_extension": "mp4"}
]
```

Then run the script by entering `python main.py` in your console.
