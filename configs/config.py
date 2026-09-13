"""
Global Configuration
"""

from pathlib import Path

# ==========================
# Base Directory
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Project Folders
# ==========================
VIDEO_FOLDER = BASE_DIR / "videos"
FRAME_FOLDER = BASE_DIR / "extracted_frames"
OUTPUT_FOLDER = BASE_DIR / "output"

# Motion Detection Folder
MOTION_FOLDER = BASE_DIR / "motion_frames"

# ==========================
# Video Processing
# ==========================
FRAME_SAMPLE_RATE = 5

# ==========================
# Motion Detection
# ==========================
MOTION_THRESHOLD = 35
MIN_CONTOUR_AREA = 5000

# Object Detection
DETECTED_FRAME_FOLDER = BASE_DIR/"detected_frames"
DETECTION_JSON_FOLDER = BASE_DIR/"detections"
PERSON_CONFIDENCE = 0.50
VEHICLE_CONFIDENCE = 0.50

# Clip Extraction
BEFORE_EVENT_SECONDS = 10
AFTER_EVENT_SECONDS = 20

CLIPS_FOLDER = BASE_DIR/"clips"
CLIPS_FOLDER.mkdir(parents=True,exist_ok=True)

# SUMMARY GENERATION

SUMMARY_FOLDER = BASE_DIR / "output"
SUMMARY_VIDEO_NAME = "summary.mp4"
SUMMARY_VIDEO_PATH = SUMMARY_FOLDER / SUMMARY_VIDEO_NAME



DETECTED_FRAMES_FOLDER = Path("detected_frames")

DETECTIONS_FOLDER = Path("detections")

MOTION_FRAMES_FOLDER = BASE_DIR / "motion_frames"
DETECTIONS_FOLDER = BASE_DIR / "detections"