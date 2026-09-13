from pathlib import Path
import json

from processors.frame_extractor import FrameExtractor
from detectors.motion_detector import MotionDetector
from detectors.object_detector import ObjectDetector

from tracker.object_tracker import CentroidTracker
from event_detection.event_detector import EventDetector

from clip_extraction.clip_extractor import ClipExtractor
from summary_generation.summary_generator import SummaryGenerator
from timeline.timeline_generator import TimelineGenerator
from reports.report_generator import ReportGenerator
from configs.config import DETECTIONS_FOLDER

def run_pipeline(video_path):
    video_path = Path(video_path)

    print("=" * 50)
    print("AI VIDEO SUMMARIZATION SYSTEM")
    print("=" * 50)

    # ==========================================
    # INPUT VIDEO
    # ==========================================

    

    print(
        "Video Path:",
        video_path
    )

    print(
        "Absolute Path:",
        video_path.resolve()
    )

    print(
        "Video Exists:",
        video_path.exists()
    )

    if not video_path.exists():

        raise FileNotFoundError(
            f"Video not found: "
            f"{video_path.resolve()}"
        )

    print()
    print("Input video found successfully!")

    # ==========================================
    # STEP 2: FRAME EXTRACTION
    # ==========================================

    print()
    print("=" * 50)
    print("STEP 2: FRAME EXTRACTION")
    print("=" * 50)

    extractor = FrameExtractor(
        video_path,
        5
    )

    extractor.extract_frames()

    print()
    print("Frame extraction completed!")

    # ==========================================
    # STEP 3: MOTION DETECTION
    # ==========================================

    print()
    print("=" * 50)
    print("STEP 3: MOTION DETECTION")
    print("=" * 50)


    


    motion_detector = MotionDetector(
        save_every_n_motion_frames=5
    )


    motion_detector.detect_motion(
        video_path
    )


    print()
    print("Motion detection completed!")

    # ==========================================
    # STEP 4: OBJECT DETECTION
    # ==========================================


    print("\n")
    print("=" * 50)
    print("STEP 4: OBJECT DETECTION")
    print("=" * 50)

    object_detector = ObjectDetector()

    detections = object_detector.detect_objects()

    
    # ============================================================
    # STEP 5: OBJECT TRACKING + EVENT DETECTION
    # ============================================================

    print()
    print("=" * 50)
    print("STEP 5: OBJECT TRACKING + EVENT DETECTION")
    print("=" * 50)


    # ============================================================
    # CREATE TRACKER
    # ============================================================

    tracker = CentroidTracker(
        max_distance=80,
        max_disappeared=5
    )


    # ============================================================
    # CREATE EVENT DETECTOR
    # ============================================================

    event_detector = EventDetector()


    # ============================================================
    # FIND DETECTION FILES
    # ============================================================

    detection_files = sorted(
        Path(DETECTIONS_FOLDER).glob("*.json")
    )

    print(
        "Detection files found:",
        len(detection_files)
    )


    # ============================================================
    # PROCESS DETECTIONS
    # ============================================================

    all_events = []


    for detection_file in detection_files:

        print()
        print(
            "Processing:",
            detection_file.name
        )


        # --------------------------------------------------------
        # READ JSON
        # --------------------------------------------------------

        with open(
            detection_file,
            "r",
            encoding="utf-8"
        ) as file:

            detection_data = json.load(file)


        # --------------------------------------------------------
        # GET REAL TIMESTAMP
        # --------------------------------------------------------

        timestamp = detection_data.get(
            "timestamp",
            0.0
        )


        # --------------------------------------------------------
        # GET DETECTIONS
        # --------------------------------------------------------

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


        # --------------------------------------------------------
        # TRACK OBJECTS
        # --------------------------------------------------------

        tracked_objects = tracker.update(
            detections
        )


        print(
            "Tracked objects:",
            len(tracked_objects)
        )


        # --------------------------------------------------------
        # DETECT EVENTS
        # --------------------------------------------------------

        events = event_detector.detect_events(
            tracked_objects,
            timestamp
        )


        # --------------------------------------------------------
        # PRINT EVENTS
        # --------------------------------------------------------

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

            all_events.extend(
                events
            )


    # ============================================================
    # STEP 5 FINAL RESULTS
    # ============================================================

    print()
    print("=" * 50)
    print("TRACKING + EVENT DETECTION COMPLETE")
    print("=" * 50)

    print(
        "Total meaningful events:",
        len(all_events)
    )

    print("=" * 50)


    # ============================================================
    # STEP 6: EVENT-BASED CLIP EXTRACTION
    # ============================================================

    print()
    print("=" * 50)
    print("STEP 6: EVENT-BASED CLIP EXTRACTION")
    print("=" * 50)


    # ============================================================
    # CREATE CLIP EXTRACTOR
    # ============================================================

    clip_extractor = ClipExtractor()


    # ============================================================
    # VIDEO PATH
    # ============================================================




    # ============================================================
    # EXTRACT CLIPS
    # ============================================================

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


        # --------------------------------------------------------
        # CREATE CLIP
        # --------------------------------------------------------

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

            print(
                error
            )


    # ============================================================
    # STEP 6 FINAL RESULTS
    # ============================================================

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


    # --------------------------------------------------
    # STEP 8 COMPLETE
    # --------------------------------------------------

    print()
    print("=" * 50)
    print("STEP 8 COMPLETE")
    print("=" * 50)

###*************STEP 9
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

    return {
        "status": "success",
        "message": "Video analysis completed successfully.",
        "summary": str(summary_path) if "summary_path" in locals() else None,
        "timeline": str(timeline_path) if "timeline_path" in locals() else None,
        "report": str(report_path) if "report_path" in locals() else None,
        "clips": [str(path) for path in clip_paths]
    }

    print()
    print("=" * 50)
    print("STEP 9 COMPLETE")
    print("=" * 50)

if __name__ == "__main__":

    default_video = Path(
        "videos/sample.mp4"
    )

    run_pipeline(
        default_video
    )

