from pathlib import Path
import json

from tracker.object_tracker import CentroidTracker
from event_detection.event_detector import EventDetector
from clip_extraction.clip_extractor import ClipExtractor
from summary_generation.summary_generator import SummaryGenerator
from timeline.timeline_generator import TimelineGenerator
from configs.config import DETECTIONS_FOLDER
from reports.report_generator import ReportGenerator


print()
print("=" * 50)
print("STEP 6: EVENT-BASED CLIP EXTRACTION")
print("=" * 50)


# --------------------------------------------------
# 1. CREATE TRACKER
# --------------------------------------------------

tracker = CentroidTracker(
    max_distance=80,
    max_disappeared=5
)


# --------------------------------------------------
# 2. CREATE EVENT DETECTOR
# --------------------------------------------------

event_detector = EventDetector()


# --------------------------------------------------
# 3. CREATE CLIP EXTRACTOR
# --------------------------------------------------

clip_extractor = ClipExtractor()


# --------------------------------------------------
# 4. FIND DETECTION FILES
# --------------------------------------------------

detection_files = sorted(
    Path(DETECTIONS_FOLDER).glob("*.json")
)

print(
    "Detection files found:",
    len(detection_files)
)


# Store all events
all_events = []


# --------------------------------------------------
# 5. TRACK + DETECT EVENTS
# --------------------------------------------------

for detection_file in detection_files:

    print()
    print(
        "Processing:",
        detection_file.name
    )

    # Read detection JSON
    with open(
        detection_file,
        "r",
        encoding="utf-8"
    ) as file:

        detection_data = json.load(file)


    # Get REAL timestamp
    timestamp = detection_data.get(
        "timestamp",
        0.0
    )


    # Get detections
    detections = detection_data.get(
        "detections",
        []
    )


    print(
        "Detections found:",
        len(detections)
    )

    print(
        "Real timestamp:",
        f"{timestamp:.3f}s"
    )


    # Track objects
    tracked_objects = tracker.update(
        detections
    )


    print(
        "Tracked objects:",
        len(tracked_objects)
    )


    # Detect events
    events = event_detector.detect_events(
        tracked_objects,
        timestamp
    )


    # Store events
    if events:

        print(
            "Events detected:",
            len(events)
        )

        for event in events:

            print(
                f"  {event['timestamp']:.3f}s | "
                f"{event['event']} | "
                f"class: {event['class']} | "
                f"count: {event['count']}"
            )

        all_events.extend(events)


# --------------------------------------------------
# 6. CLIP EXTRACTION
# --------------------------------------------------

print()
print("=" * 50)
print("EXTRACTING EVENT CLIPS")
print("=" * 50)


video_path = Path(
    "videos/sample.mp4"
)


clip_paths = []


for clip_number, event in enumerate(
    all_events,
    start=1
):

    event_time = event.get(
        "timestamp",
        0.0
    )

    event_name = event.get(
        "event",
        "Unknown Event"
    )


    print()
    print(
        f"Clip {clip_number}"
    )

    print(
        "Event:",
        event_name
    )

    print(
        "Timestamp:",
        f"{event_time:.2f}s"
    )


    try:

        clip_path = clip_extractor.extract_clip(
            video_path=video_path,
            event_time=event_time,
            event_name=event_name,
            clip_number=clip_number
        )

        clip_paths.append(
            clip_path
        )

    except Exception as error:

        print(
            "Clip extraction failed:"
        )

        print(error)


# --------------------------------------------------
# 7. FINAL RESULT
# --------------------------------------------------

print()
print("=" * 50)
print("STEP 6 COMPLETE")
print("=" * 50)

print(
    "Total events:",
    len(all_events)
)

print(
    "Clips successfully created:",
    len(clip_paths)
)

for clip_path in clip_paths:

    print(
        "  ",
        clip_path
    )

print("=" * 50)


# ============================================================
# STEP 7: SUMMARY VIDEO GENERATION
# ============================================================

print()
print("=" * 50)
print("STEP 7: SUMMARY VIDEO GENERATION")
print("=" * 50)


# --------------------------------------------------
# CREATE SUMMARY GENERATOR
# --------------------------------------------------

summary_generator = SummaryGenerator()


# --------------------------------------------------
# CREATE SUMMARY
# --------------------------------------------------

try:

    summary_path = summary_generator.create_summary(
        clip_paths
    )

    print()
    print(
        "Summary video successfully created!"
    )

    print(
        "Summary path:",
        summary_path
    )

except Exception as error:

    print()
    print(
        "Summary generation failed:"
    )

    print(
        error
    )


# --------------------------------------------------
# STEP 7 COMPLETE
# --------------------------------------------------

print()
print("=" * 50)
print("STEP 7 COMPLETE")
print("=" * 50)

# ============================================================
# STEP 8: TIMELINE GENERATION
# ============================================================

print()
print("=" * 50)
print("STEP 8: TIMELINE GENERATION")
print("=" * 50)


# --------------------------------------------------
# CREATE TIMELINE GENERATOR
# --------------------------------------------------

timeline_generator = TimelineGenerator()


# --------------------------------------------------
# GENERATE TIMELINE
# --------------------------------------------------

try:

    timeline_path = timeline_generator.generate_timeline(
        all_events
    )

    print()
    print(
        "Timeline successfully created!"
    )

    print(
        "Timeline path:",
        timeline_path
    )

except Exception as error:

    print()
    print(
        "Timeline generation failed:"
    )

    print(
        error
    )

print()
print("=" * 50)
print("STEP 9: REPORT GENERATION")
print("=" * 50)

report_generator = ReportGenerator()

try:

    report_path = report_generator.generate_report(
        all_events
    )

    print()
    print(
        "Report successfully created!"
    )

    print(
        "Report path:",
        report_path
    )

except Exception as error:

    print()
    print(
        "Report generation failed:"
    )

    print(error)

print()
print("=" * 50)
print("STEP 9 COMPLETE")
print("=" * 50)