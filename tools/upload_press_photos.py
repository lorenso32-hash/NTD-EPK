"""
Upload NightTimeDrive press photo previews to Cloudinary (folder: NTD/Press).

Usage: python3 tools/upload_press_photos.py "path/one.jpg" "path/two.jpg"

Prints one line per photo to paste into the PRESS_PHOTOS array in index.html.
Credentials are read from "Luz By LJ/.env" (same Cloudinary account).
"""
import re, sys, json
from pathlib import Path

import cloudinary, cloudinary.uploader
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parent.parent
env = dotenv_values(ROOT / "Luz By LJ" / ".env")
cloudinary.config(
    cloud_name=env["CLOUDINARY_CLOUD_NAME"],
    api_key=env["CLOUDINARY_API_KEY"],
    api_secret=env["CLOUDINARY_API_SECRET"],
    secure=True,
)

if len(sys.argv) < 2:
    sys.exit(__doc__)

for arg in sys.argv[1:]:
    path = Path(arg)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", path.stem).strip("_")
    res = cloudinary.uploader.upload(
        str(path), public_id=f"NTD/Press/{slug}", overwrite=True, resource_type="image"
    )
    entry = {"id": res["public_id"], "w": res["width"], "h": res["height"], "alt": "NightTimeDrive press photo"}
    print(json.dumps(entry) + ",")
