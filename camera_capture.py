#!/usr/bin/env python3

import argparse
import multiprocessing as mp
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture camera frames periodically and save as JPEG."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Capture interval in seconds (default: 1.0)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./Data/Camera",
        help="Directory to save captured images (default: ./Data/Camera)",
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="OpenCV camera index (default: 0)",
    )
    parser.add_argument(
        "--camera-indices",
        type=str,
        default="",
        help="Comma-separated OpenCV camera indices (e.g. 2,4,5). If set, overrides --camera-index.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=0,
        help="Stop after N frames (0 = infinite, default: 0)",
    )
    return parser.parse_args()


def timestamp_name() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.000Z")


def run_opencv(interval: float, output_dir: str, camera_index: int, max_frames: int) -> None:
    import cv2  # type: ignore

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open camera index {camera_index} with OpenCV")

    print(f"[INFO] OpenCV camera opened (index={camera_index})")
    frame_count = 0
    try:
        while True:
            ok, frame = cap.read()
            if not ok or frame is None:
                print("[WARN] Failed to read frame from camera")
                time.sleep(interval)
                continue

            name = f"{timestamp_name()}.jpg"
            path = os.path.join(output_dir, name)
            if cv2.imwrite(path, frame):
                frame_count += 1
                print(f"[SAVE] {path}")
            else:
                print(f"[WARN] Failed to write image: {path}")

            if max_frames > 0 and frame_count >= max_frames:
                print(f"[INFO] Reached max-frames={max_frames}, stopping.")
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        cap.release()


def run_picamera2(interval: float, output_dir: str, max_frames: int) -> None:
    from picamera2 import Picamera2  # type: ignore

    camera = Picamera2()
    config = camera.create_still_configuration()
    camera.configure(config)
    camera.start()
    time.sleep(0.5)

    print("[INFO] Picamera2 started")
    frame_count = 0
    try:
        while True:
            name = f"{timestamp_name()}.jpg"
            path = os.path.join(output_dir, name)
            camera.capture_file(path)
            frame_count += 1
            print(f"[SAVE] {path}")

            if max_frames > 0 and frame_count >= max_frames:
                print(f"[INFO] Reached max-frames={max_frames}, stopping.")
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        camera.stop()


def run_camera_cli(interval: float, output_dir: str, max_frames: int) -> None:
    cli = shutil.which("rpicam-still") or shutil.which("libcamera-still")
    if cli is None:
        raise RuntimeError("Neither rpicam-still nor libcamera-still command is available")

    print(f"[INFO] Camera CLI backend started ({os.path.basename(cli)})")
    frame_count = 0
    try:
        while True:
            name = f"{timestamp_name()}.jpg"
            path = os.path.join(output_dir, name)
            cmd = [cli, "-n", "-t", "1", "-o", path]
            completed = subprocess.run(cmd, capture_output=True, text=True)
            if completed.returncode != 0:
                err_msg = completed.stderr.strip() or completed.stdout.strip() or "unknown error"
                print(f"[WARN] Camera CLI capture failed: {err_msg}")
            else:
                frame_count += 1
                print(f"[SAVE] {path}")

            if max_frames > 0 and frame_count >= max_frames:
                print(f"[INFO] Reached max-frames={max_frames}, stopping.")
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")


def parse_indices(camera_indices: str, camera_index: int) -> List[int]:
    if not camera_indices.strip():
        return [camera_index]
    values: List[int] = []
    for token in camera_indices.split(","):
        token = token.strip()
        if not token:
            continue
        values.append(int(token))
    if not values:
        raise SystemExit("--camera-indices is empty")
    return values


def run_for_single_index(
    interval: float,
    max_frames: int,
    output_dir: str,
    index: int,
    multi_index: bool,
) -> None:
    single_output_dir = output_dir
    if multi_index:
        single_output_dir = os.path.join(output_dir, f"cam_{index}")
        os.makedirs(single_output_dir, exist_ok=True)

    print(f"\n=== Camera index {index} ===")
    print(f"Output directory: {single_output_dir}")
    try:
        run_opencv(interval, single_output_dir, index, max_frames)
    except Exception as opencv_err:
        print(f"[WARN] OpenCV path failed: {opencv_err}")
        print("[INFO] Trying Picamera2 backend...")
        try:
            run_picamera2(interval, single_output_dir, max_frames)
        except Exception as picam_err:
            print(f"[WARN] Picamera2 path failed: {picam_err}")
            print("[INFO] Trying camera CLI backend (rpicam-still/libcamera-still)...")
            try:
                run_camera_cli(interval, single_output_dir, max_frames)
            except Exception as cli_err:
                print(
                    "Camera capture failed on all backends.\n"
                    f"- OpenCV error: {opencv_err}\n"
                    f"- Picamera2 error: {picam_err}\n"
                    f"- Camera CLI error: {cli_err}"
                )


def run_parallel_capture(indices: List[int], interval: float, max_frames: int, output_dir: str) -> None:
    multi_index = len(indices) > 1
    processes: List[mp.Process] = []

    for index in indices:
        process = mp.Process(
            target=run_for_single_index,
            args=(interval, max_frames, output_dir, index, multi_index),
            daemon=False,
        )
        process.start()
        processes.append(process)

    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("\n[INFO] Stopping all camera capture processes...")
        for process in processes:
            if process.is_alive():
                process.terminate()
        for process in processes:
            process.join()


def main() -> None:
    args = parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval must be > 0")
    if args.max_frames < 0:
        raise SystemExit("--max-frames must be >= 0")

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    indices = parse_indices(args.camera_indices, args.camera_index)

    print("Start camera capture. Press Ctrl+C to stop.")
    print(f"Base output directory: {output_dir}")
    print(f"Camera indices: {indices}")
    print(f"Interval: {args.interval}s, max-frames: {args.max_frames}")
    run_parallel_capture(indices, args.interval, args.max_frames, output_dir)


if __name__ == "__main__":
    main()
