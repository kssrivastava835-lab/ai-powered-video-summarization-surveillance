from pathlib import Path
import json
import uuid
import shutil

from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from main import run_pipeline
# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VIDEOS_FOLDER = BASE_DIR / "videos"

OUTPUT_FOLDER = BASE_DIR / "output"

SUMMARY_PATH = OUTPUT_FOLDER / "summary.mp4"

TIMELINE_PATH = (
    OUTPUT_FOLDER
    / "timeline"
    / "timeline.json"
)

REPORT_PATH = (
    OUTPUT_FOLDER
    / "reports"
    / "surveillance_report.json"
)

CLIPS_FOLDER = BASE_DIR / "clips"


# ============================================================
# CREATE FOLDERS
# ============================================================

VIDEOS_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

CLIPS_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# ============================================================
# ANALYSIS JOBS
# ============================================================

analysis_jobs = {}

# ============================================================
# CLEAN OLD ANALYSIS DATA
# ============================================================

def clean_previous_analysis():

    folders_to_clean = [
        BASE_DIR / "frames",
        BASE_DIR / "motion_frames",
        BASE_DIR / "detections",
        BASE_DIR / "clips",
        OUTPUT_FOLDER / "timeline",
        OUTPUT_FOLDER / "reports"
    ]

    files_to_remove = [
        SUMMARY_PATH
    ]

    for folder in folders_to_clean:

        if folder.exists():

            for item in folder.iterdir():

                if item.is_file() or item.is_symlink():
                    item.unlink()

                elif item.is_dir():
                    shutil.rmtree(item)

    for file_path in files_to_remove:

        if file_path.exists():
            file_path.unlink()

def run_analysis_job(job_id, video_path, filename):

    try:

        analysis_jobs[job_id]["status"] = "processing"

        clean_previous_analysis()

        result = run_pipeline(video_path)

        analysis_jobs[job_id]["status"] = "completed"
        analysis_jobs[job_id]["result"] = result

    except Exception as error:

        analysis_jobs[job_id]["status"] = "failed"
        analysis_jobs[job_id]["error"] = str(error)



# ============================================================
# CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="AI Surveillance API",
    description=(
        "FastAPI backend for the "
        "AI-Powered Video Summarization "
        "for Surveillance system."
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "AI Surveillance API is running",
        "status": "success"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "service": "AI Surveillance API"
    }


# ============================================================
# UPLOAD VIDEO
# ============================================================

@app.post("/upload-video")
async def upload_video(
    file: UploadFile = File(...)
):

    if not file.filename:

        return {
            "status": "error",
            "message": "No file provided."
        }

    allowed_extensions = {
        ".mp4",
        ".avi",
        ".mov",
        ".mkv"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        return {
            "status": "error",
            "message": (
                "Unsupported video format. "
                "Use MP4, AVI, MOV or MKV."
            )
        }

    output_path = (
        VIDEOS_FOLDER
        / file.filename
    )

    with open(
        output_path,
        "wb"
    ) as video_file:

        while True:

            chunk = await file.read(
                1024 * 1024
            )

            if not chunk:
                break

            video_file.write(chunk)

    return {
        "status": "success",
        "message": "Video uploaded successfully.",
        "filename": file.filename,
        "path": str(output_path)
    }

# ============================================================
# START VIDEO ANALYSIS
# ============================================================

@app.post("/analyze")
def analyze_video(
    filename: str,
    background_tasks: BackgroundTasks
):

    video_path = VIDEOS_FOLDER / filename

    if not video_path.exists():

        return {
            "status": "error",
            "message": "Video not found.",
            "filename": filename
        }

    job_id = str(uuid.uuid4())

    analysis_jobs[job_id] = {
        "status": "queued",
        "filename": filename
    }

    background_tasks.add_task(
        run_analysis_job,
        job_id,
        video_path,
        filename
    )

    return {
        "status": "accepted",
        "message": "Video analysis started.",
        "filename": filename,
        "job_id": job_id
    }

# ============================================================
# GET ANALYSIS STATUS
# ============================================================

@app.get("/analysis-status/{job_id}")
def get_analysis_status(job_id: str):

    if job_id not in analysis_jobs:

        return {
            "status": "error",
            "message": "Job not found.",
            "job_id": job_id
        }

    return {
        "job_id": job_id,
        **analysis_jobs[job_id]
    }



# ============================================================
# GET REPORT
# ============================================================

@app.get("/report")
def get_report():

    if not REPORT_PATH.exists():

        return {
            "status": "error",
            "message": "Report not found."
        }

    with open(
        REPORT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        report = json.load(file)

    return report


# ============================================================
# GET TIMELINE
# ============================================================

@app.get("/timeline")
def get_timeline():

    if not TIMELINE_PATH.exists():

        return {
            "status": "error",
            "message": "Timeline not found."
        }

    with open(
        TIMELINE_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        timeline = json.load(file)

    return timeline


# ============================================================
# GET SUMMARY VIDEO
# ============================================================

@app.get("/summary")
def get_summary():

    if not SUMMARY_PATH.exists():

        return {
            "status": "error",
            "message": "Summary video not found."
        }

    return FileResponse(
        path=SUMMARY_PATH,
        media_type="video/mp4",
        filename="summary.mp4"
    )


# ============================================================
# GET EVENT CLIPS
# ============================================================

@app.get("/clips")
def get_clips():

    if not CLIPS_FOLDER.exists():

        return {
            "status": "error",
            "message": "Clips folder not found."
        }

    clips = sorted(
        CLIPS_FOLDER.glob("*.mp4")
    )

    return {
        "total_clips": len(clips),
        "clips": [
            {
                "filename": clip.name,
                "path": str(clip)
            }
            for clip in clips
        ]
    }


# ============================================================
# GET ORIGINAL VIDEOS
# ============================================================

@app.get("/videos")
def get_videos():

    videos = sorted(
        VIDEOS_FOLDER.glob("*")
    )

    video_files = [
        video
        for video in videos
        if video.suffix.lower()
        in {
            ".mp4",
            ".avi",
            ".mov",
            ".mkv"
        }
    ]

    return {
        "total_videos": len(video_files),
        "videos": [
            {
                "filename": video.name,
                "path": str(video)
            }
            for video in video_files
        ]
    }