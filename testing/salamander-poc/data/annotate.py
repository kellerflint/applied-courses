"""
Annotate a video with YOLO detections.

Reads a video file frame by frame, runs YOLO on each frame, draws the
bounding boxes, and writes the annotated frames to a new video file.

This is the proof-of-concept for the backend video pipeline in the
Salamander Tracker midterm. The default model is yolov8n.pt (COCO classes).
Pass -m with your own trained .pt file when you have one.
"""

import argparse
import sys
from pathlib import Path

import cv2
from ultralytics import YOLO


def annotate_video(
    input_path: Path,
    output_path: Path,
    model_path: str,
    max_seconds: float | None = None,
) -> None:
    # Ultralytics auto-downloads yolov8n.pt on first use if you pass a model name
    # rather than a local path.
    model = YOLO(model_path)

    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        sys.exit(f"Could not open video: {input_path}")

    # Read source video properties so the output matches.
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # If a duration cap was passed, stop after that many seconds of source video.
    if max_seconds is not None:
        total_to_process = min(total, int(round(fps * max_seconds)))
    else:
        total_to_process = total

    # avc1 is H.264 and produces files that play in QuickTime, Chrome, and
    # everywhere else. Falls back to mp4v if the OpenCV build doesn't ship
    # H.264 support.
    out = _make_writer(output_path, fps, width, height)
    if out is None:
        cap.release()
        sys.exit(f"Could not open output writer for: {output_path}")

    print(f"Processing {total_to_process} frames at {width}x{height} @ {fps:.1f}fps")

    frame_idx = 0
    try:
        while frame_idx < total_to_process:
            ok, frame = cap.read()
            if not ok:
                break

            # Run YOLO on this single frame.
            results = model(frame, verbose=False)

            # plot() returns a numpy array (BGR) with boxes and labels drawn on it.
            annotated = results[0].plot()

            out.write(annotated)

            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"  {frame_idx}/{total_to_process} frames")
    finally:
        # Always release, even on Ctrl+C or exception. mp4 needs the writer
        # finalized to write the moov atom; without this the file won't play.
        cap.release()
        out.release()

    print(f"Wrote {frame_idx} annotated frames to {output_path}")


def _make_writer(output_path: Path, fps: float, width: int, height: int):
    for codec in ("avc1", "mp4v"):
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        if writer.isOpened():
            print(f"Using codec: {codec}")
            return writer
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to the input video file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output.mp4"),
        help="Path for the annotated output video (default: output.mp4)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default="yolov8n.pt",
        help="YOLO model file or name (default: yolov8n.pt)",
    )
    parser.add_argument(
        "-s",
        "--seconds",
        type=float,
        default=None,
        help="Only process the first N seconds of the input (default: full video)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        sys.exit(f"Input file not found: {args.input}")

    annotate_video(args.input, args.output, args.model, args.seconds)


if __name__ == "__main__":
    main()
