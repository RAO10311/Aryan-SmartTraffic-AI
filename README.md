# Aryan SmartTraffic AI 🚦

**AI-Based Traffic Monitoring & Vehicle Analytics using Computer Vision**

Aryan SmartTraffic AI is a student learning project that analyzes an uploaded road-traffic video, detects common vehicle classes, tracks vehicles across frames, and produces an annotated output video with a unique-vehicle count.

> **Project scope:** This repository contains a practical video-based prototype. It is inspired by intelligent-transportation and traffic-analytics workflows, but it does not recreate the Valdrada simulator, synthetic multi-camera dataset pipeline, segmentation masks, depth maps, or RF-DETR training workflow.

## Features

- Upload an MP4, AVI, or MOV traffic video through a web interface.
- Detect cars, motorcycles, buses, and trucks with a pretrained YOLOv8 model.
- Track detections across frames using ByteTrack.
- Draw bounding boxes and track IDs on the processed video.
- Count unique vehicle track IDs observed in the uploaded clip.
- Download and review the annotated output video.

## Tech stack

- Python
- Flask
- OpenCV
- Ultralytics YOLOv8
- ByteTrack
- HTML, CSS, JavaScript

## Project structure

```text
Aryan-SmartTraffic-AI/
├── app.py
├── requirements.txt
├── start.bat
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    ├── script.js
    └── results/
```

## Run locally (Windows)

1. Install Python 3.10 or 3.11.
2. Download or clone this repository.
3. Open PowerShell in the project folder.
4. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

The first run may take longer because Ultralytics downloads the pretrained YOLOv8n model. Processing time depends on video length and computer hardware.

## Notes

- Use short sample clips for initial testing.
- The app processes uploaded videos locally; it is not a hosted public demo.
- The vehicle count is the number of distinct tracker IDs observed during that clip. Tracking IDs can occasionally change, so this is an estimate rather than a guaranteed real-world count.
- This is an educational prototype, not a traffic-enforcement or safety-critical system.
- Do not upload private or sensitive footage without permission.

## Reference and inspiration

The project direction was inspired by the traffic-simulation and analytics work shared in the following references:

- [Primary LinkedIn reference](https://lnkd.in/e8s4fEVk)
- [Additional LinkedIn reference](https://lnkd.in/ec2Gn-fv)
- [Original Valdrada traffic-safety repository](https://github.com/CondadosAI/condados-lab/tree/main/valdrada-traffic-safety)

The references above are credited as inspiration. This repository is a separate student implementation with a narrower feature set.

## Author

**Aryan Yadav**

A learning project exploring Python, computer vision, object detection, and intelligent transportation systems.
