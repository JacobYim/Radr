"""Load SSD / local buffer paths from optional JSON (package share or RADR_PATH_CONFIG)."""

from __future__ import annotations

import json
import os
from typing import Any, Dict

DEFAULT_SSD_BASE = "/mnt/extreme-ssd"
DEFAULT_LOCAL_BASE = "/home/radr/Radr/Data/local_buffer"


def load_radr_paths() -> Dict[str, str]:
    """Merge defaults with JSON from env or radr_sensor_hub share/config/radr_paths.json."""
    out: Dict[str, Any] = {
        "ssd_base": DEFAULT_SSD_BASE,
        "local_base": DEFAULT_LOCAL_BASE,
    }
    for path in _config_file_candidates():
        if not path or not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        if not isinstance(data, dict):
            continue
        if isinstance(data.get("ssd_base"), str) and data["ssd_base"].strip():
            out["ssd_base"] = data["ssd_base"].strip()
        if isinstance(data.get("local_base"), str) and data["local_base"].strip():
            out["local_base"] = data["local_base"].strip()
        break
    return {"ssd_base": str(out["ssd_base"]), "local_base": str(out["local_base"])}


def _config_file_candidates() -> list[str | None]:
    env_path = os.environ.get("RADR_PATH_CONFIG")
    found: list[str | None] = []
    if env_path:
        found.append(env_path)
    try:
        from ament_index_python.packages import get_package_share_directory

        share = get_package_share_directory("radr_sensor_hub")
        found.append(os.path.join(share, "config", "radr_paths.json"))
    except Exception:
        pass
    return found
