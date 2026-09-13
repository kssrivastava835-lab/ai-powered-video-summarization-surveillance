from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip

from configs.config import (
    CLIPS_FOLDER,
    BEFORE_EVENT_SECONDS,
    AFTER_EVENT_SECONDS
)


class ClipExtractor:

    def __init__(self):

        CLIPS_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

    def extract_clip(
        self,
        video_path,
        event_time,
        event_name,
        clip_number
    ):

        video_path = Path(video_path)

        if not video_path.exists():

            raise FileNotFoundError(
                f"Video not found: "
                f"{video_path.resolve()}"
            )

        print()
        print("=" * 50)
        print("CLIP EXTRACTION")
        print("=" * 50)

        print(
            "Event:",
            event_name
        )

        print(
            "Event Time:",
            event_time,
            "seconds"
        )

        video = VideoFileClip(
            str(video_path)
        )

        # Time before the event
        start_time = max(
            0,
            event_time - BEFORE_EVENT_SECONDS
        )

        # Time after the event
        end_time = min(
            video.duration,
            event_time + AFTER_EVENT_SECONDS
        )

        print(
            "Clip Start:",
            start_time
        )

        print(
            "Clip End:",
            end_time
        )

        # Create the subclip
        clip = video.subclipped(
            start_time,
            end_time
        )

        # Make event name safe for filename
        safe_event_name = (
            event_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_path = (
            CLIPS_FOLDER /
            f"{clip_number:03d}_"
            f"{safe_event_name}.mp4"
        )

        print(
            "Saving:",
            output_path
        )

        clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio_codec="aac"
        )

        clip.close()
        video.close()

        print(
            f"Clip saved: {output_path}"
        )

        print("=" * 50)

        return output_path