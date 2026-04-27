from datetime import datetime, timezone

from std_msgs.msg import String


def utc_now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def publish_log(log_pub, source: str, level: str, message: str) -> None:
    stamp = utc_now_text()
    payload = f"[{stamp}] [{level}] [{source}] {message}"
    log_pub.publish(String(data=payload))
