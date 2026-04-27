import os
import shutil
from threading import Lock
from typing import Optional


class SessionStorage:
    def __init__(self, session_id: str, subdir: str) -> None:
        self.session_id = session_id
        self.subdir = subdir
        self.ssd_base = "/media/radr/Extreme SSD"
        self.local_base = "/home/radr/Radr/Data/local_buffer"
        self.lock = Lock()

        self.local_dir = os.path.join(self.local_base, self.session_id, self.subdir)
        os.makedirs(self.local_dir, exist_ok=True)
        self._last_target: Optional[str] = None

    def _ssd_ready(self) -> bool:
        return os.path.isdir(self.ssd_base) and os.access(self.ssd_base, os.W_OK)

    def _ssd_dir(self) -> str:
        return os.path.join(self.ssd_base, self.session_id, self.subdir)

    def _migrate_local_files(self) -> None:
        if not self._ssd_ready():
            return
        ssd_dir = self._ssd_dir()
        os.makedirs(ssd_dir, exist_ok=True)
        if not os.path.isdir(self.local_dir):
            return
        for name in os.listdir(self.local_dir):
            src = os.path.join(self.local_dir, name)
            dst = os.path.join(ssd_dir, name)
            if not os.path.isfile(src):
                continue
            if os.path.exists(dst):
                base, ext = os.path.splitext(name)
                idx = 1
                while True:
                    candidate = os.path.join(ssd_dir, f"{base}_{idx}{ext}")
                    if not os.path.exists(candidate):
                        dst = candidate
                        break
                    idx += 1
            shutil.move(src, dst)

    def get_output_dir(self) -> str:
        with self.lock:
            if self._ssd_ready():
                ssd_dir = self._ssd_dir()
                os.makedirs(ssd_dir, exist_ok=True)
                self._migrate_local_files()
                self._last_target = ssd_dir
                return ssd_dir
            self._last_target = self.local_dir
            return self.local_dir

    def describe_target(self) -> str:
        with self.lock:
            if self._ssd_ready():
                return self._ssd_dir()
            return self.local_dir
