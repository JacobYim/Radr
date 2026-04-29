import os
import shutil

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .logging_utils import publish_log
from .time_utils import now_et


class SyncNode(Node):
    def __init__(self) -> None:
        super().__init__("sync_node")
        self.declare_parameter("session_id", "session_unknown")
        self.declare_parameter("interval_sec", 10.0)
        self.declare_parameter("ssd_base", "/media/radr/Extreme SSD")
        self.declare_parameter("local_base", "/home/radr/Radr/Data/local_buffer")
        self.declare_parameter("retention_sec", 300.0)

        self.session_id = self.get_parameter("session_id").get_parameter_value().string_value
        self.interval = self.get_parameter("interval_sec").get_parameter_value().double_value
        self.ssd_base = self.get_parameter("ssd_base").get_parameter_value().string_value
        self.local_base = self.get_parameter("local_base").get_parameter_value().string_value
        self.retention_sec = self.get_parameter("retention_sec").get_parameter_value().double_value
        self.log_pub = self.create_publisher(String, "/system/log", 100)

        self.timer = self.create_timer(self.interval, self.sync_once)
        publish_log(self.log_pub, "sync_node", "INFO", "Node started")

    def prune_local_buffer(self) -> None:
        if self.retention_sec <= 0 or not os.path.isdir(self.local_base):
            return

        cutoff = now_et().timestamp() - self.retention_sec
        removed_files = 0

        for root, _, files in os.walk(self.local_base):
            for name in files:
                path = os.path.join(root, name)
                try:
                    if os.path.getmtime(path) < cutoff:
                        os.remove(path)
                        removed_files += 1
                except OSError:
                    continue

        # Remove empty directories after file pruning.
        for root, dirs, _ in os.walk(self.local_base, topdown=False):
            for name in dirs:
                path = os.path.join(root, name)
                try:
                    if not os.listdir(path):
                        os.rmdir(path)
                except OSError:
                    continue

        if removed_files > 0:
            publish_log(
                self.log_pub,
                "sync_node",
                "OK",
                f"Pruned {removed_files} file(s) older than {self.retention_sec:.0f}s from local buffer",
            )

    def sync_once(self) -> None:
        self.prune_local_buffer()
        if not os.path.isdir(self.ssd_base) or not os.access(self.ssd_base, os.W_OK):
            return
        local_session = os.path.join(self.local_base, self.session_id)
        if not os.path.isdir(local_session):
            return
        ssd_session = os.path.join(self.ssd_base, self.session_id)
        os.makedirs(ssd_session, exist_ok=True)

        moved = 0
        for root, _, files in os.walk(local_session):
            rel = os.path.relpath(root, local_session)
            target_root = os.path.join(ssd_session, rel) if rel != "." else ssd_session
            os.makedirs(target_root, exist_ok=True)
            for name in files:
                src = os.path.join(root, name)
                dst = os.path.join(target_root, name)
                if os.path.exists(dst):
                    base, ext = os.path.splitext(name)
                    stamp = now_et().strftime("%Y%m%d%H%M%S")
                    dst = os.path.join(target_root, f"{base}_{stamp}{ext}")
                try:
                    shutil.move(src, dst)
                    moved += 1
                except Exception:
                    continue
        if moved > 0:
            publish_log(self.log_pub, "sync_node", "OK", f"Moved {moved} file(s) to SSD")


def main() -> None:
    rclpy.init()
    node = SyncNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
