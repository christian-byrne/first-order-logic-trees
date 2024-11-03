import os

from utils.config import Config


def cleanup_temp_files(filename: str):
    proj_root = Config.get_proj_root()
    candidates = [
        proj_root / f"{filename}.png",
        proj_root / f"{filename}.gv",
        proj_root / f"{filename}",
        proj_root / "output" / f"{filename}.png",
        proj_root / "output" / f"{filename}.gv",
        proj_root / "output" / f"{filename}",
    ]
    for candidate in candidates:
        if candidate.exists():
            os.remove(candidate)
