from std_msgs.msg import String

from .time_utils import iso_et_text


def et_now_text() -> str:
    return iso_et_text()


def publish_log(log_pub, source: str, level: str, message: str) -> None:
    stamp = et_now_text()
    payload = f"[{stamp}] [{level}] [{source}] {message}"
    log_pub.publish(String(data=payload))
