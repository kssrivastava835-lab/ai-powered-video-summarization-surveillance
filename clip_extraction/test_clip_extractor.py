from pathlib import Path

from clip_extraction.clip_extractor import ClipExtractor


extractor = ClipExtractor()


video_path = Path("videos/sample.mp4")


events = [
    {
        "event": "Vehicle Appeared",
        "time": 5
    },
    {
        "event": "Fire Detected",
        "time": 10
    },
    {
        "event": "Vehicle Fire",
        "time": 15
    }
]


for i, event in enumerate(events):

    extractor.extract_clip(
        video_path,
        event["time"],
        event["event"],
        i + 1
    )