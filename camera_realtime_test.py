#!/usr/bin/env python3

import argparse
import os
from datetime import datetime

import cv2  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Real-time camera/video preview test using OpenCV."
    )
    parser.add_argument(
        "--source",
        type=str,
        default="0",
        help="Camera index (e.g. 0) or video file path (e.g. ./Data/test.mp4).",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=640,
        help="Preferred capture width (default: 640).",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Preferred capture height (default: 480).",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save preview stream to MP4 file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./Data/CameraPreview",
        help="Output directory for saved video (default: ./Data/CameraPreview).",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=20.0,
        help="Fallback FPS for saved video (default: 20).",
    )
    return parser.parse_args()


def parse_source(raw_source: str):
    source = raw_source.strip()
    return int(source) if source.isdigit() else source


def main() -> None:
    args = parse_args()
    source = parse_source(args.source)

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"카메라/영상 소스를 열 수 없습니다: {args.source}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    writer = None
    output_path = None

    if args.save:
        output_dir = os.path.abspath(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"preview_{timestamp}.mp4")

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or args.width
        frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or args.height
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps <= 1:
            fps = args.fps

        writer = cv2.VideoWriter(output_path, fourcc, fps, (frame_w, frame_h))
        if not writer.isOpened():
            cap.release()
            raise SystemExit(f"저장 파일을 열 수 없습니다: {output_path}")

        print(f"[INFO] 저장 경로: {output_path}")

    print("[INFO] 실시간 미리보기를 시작합니다. 종료하려면 'q' 키를 누르세요.")

    while True:
        ok, frame = cap.read()
        if not ok or frame is None:
            print("[WARN] 프레임을 읽을 수 없어 종료합니다.")
            break

        cv2.imshow("Camera Realtime Test (press q to quit)", frame)

        if writer is not None:
            writer.write(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()

    if output_path:
        print(f"[INFO] 저장 완료: {output_path}")


if __name__ == "__main__":
    main()
