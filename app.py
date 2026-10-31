from pathlib import Path
from uuid import uuid4

import cv2
from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
RESULT_DIR = BASE_DIR / "static" / "results"
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}
VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck (COCO)

UPLOAD_DIR.mkdir(exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB

# The pretrained model is downloaded automatically on first run if needed.
model = YOLO("yolov8n.pt")


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process_video(input_path: Path, output_path: Path) -> tuple[int, int]:
    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise ValueError("The uploaded video could not be opened.")

    fps = capture.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 25.0

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if width <= 0 or height <= 0:
        capture.release()
        raise ValueError("The video has invalid dimensions.")

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )
    if not writer.isOpened():
        capture.release()
        raise ValueError("Could not create the output video.")

    unique_ids = set()
    frame_count = 0

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break

            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=VEHICLE_CLASSES,
                conf=0.25,
                verbose=False,
            )
            result = results[0]

            if result.boxes is not None:
                for box in result.boxes:
                    if box.id is None:
                        continue
                    track_id = int(box.id.item())
                    unique_ids.add(track_id)

            annotated = result.plot()
            cv2.putText(
                annotated,
                f"Unique vehicles tracked: {len(unique_ids)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 220, 120),
                2,
                cv2.LINE_AA,
            )
            writer.write(annotated)
            frame_count += 1
    finally:
        capture.release()
        writer.release()

    if frame_count == 0:
        raise ValueError("No readable frames were found in the video.")

    return frame_count, len(unique_ids)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result_video = None
    vehicle_count = None
    frame_count = None

    if request.method == "POST":
        uploaded = request.files.get("video")
        if uploaded is None or not uploaded.filename:
            error = "Please choose a video file."
        elif not allowed_file(uploaded.filename):
            error = "Unsupported format. Please upload MP4, AVI, MOV, or MKV."
        else:
            job_id = uuid4().hex
            safe_name = secure_filename(uploaded.filename)
            input_path = UPLOAD_DIR / f"{job_id}_{safe_name}"
            output_name = f"{job_id}.mp4"
            output_path = RESULT_DIR / output_name
            uploaded.save(input_path)

            try:
                frame_count, vehicle_count = process_video(input_path, output_path)
                result_video = url_for("static", filename=f"results/{output_name}")
            except Exception as exc:
                error = f"Video processing failed: {exc}"
                if output_path.exists():
                    output_path.unlink()
            finally:
                if input_path.exists():
                    input_path.unlink()

    return render_template(
        "index.html",
        error=error,
        result_video=result_video,
        vehicle_count=vehicle_count,
        frame_count=frame_count,
    )


@app.errorhandler(413)
def file_too_large(_error):
    return render_template(
        "index.html",
        error="File is too large. Please upload a video smaller than 200 MB.",
        result_video=None,
        vehicle_count=None,
        frame_count=None,
    ), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
