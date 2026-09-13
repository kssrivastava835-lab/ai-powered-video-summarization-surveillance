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

        # --------------------------------------------------
        # CHECK VIDEO
        # --------------------------------------------------

        video_path = Path(
            video_path
        )

        if not video_path.exists():

            raise FileNotFoundError(
                f"Video not found: {video_path.resolve()}"
            )


        # --------------------------------------------------
        # PRINT EVENT INFORMATION
        # --------------------------------------------------

        print()
        print(
            f"Creating clip for: {event_name}"
        )

        print(
            "Event timestamp:",
            round(event_time, 2),
            "seconds"
        )


        # --------------------------------------------------
        # LOAD ORIGINAL VIDEO
        # --------------------------------------------------

        video = VideoFileClip(
            str(video_path)
        )


        # --------------------------------------------------
        # CALCULATE CLIP TIME
        # --------------------------------------------------

        start_time = max(
            0,
            event_time - BEFORE_EVENT_SECONDS
        )

        end_time = min(
            video.duration,
            event_time + AFTER_EVENT_SECONDS
        )


        print(
            "Clip start:",
            round(start_time, 2),
            "seconds"
        )

        print(
            "Clip end:",
            round(end_time, 2),
            "seconds"
        )


        # --------------------------------------------------
        # CREATE SUBCLIP
        # --------------------------------------------------

        clip = video.subclipped(
            start_time,
            end_time
        )


        # --------------------------------------------------
        # REMOVE AUDIO
        # --------------------------------------------------

        clip = clip.without_audio()


        # --------------------------------------------------
        # SAFE EVENT NAME
        # --------------------------------------------------

        safe_event_name = (
            event_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )


        # --------------------------------------------------
        # OUTPUT PATH
        # --------------------------------------------------

        output_path = (
            CLIPS_FOLDER
            / (
                f"{clip_number:03d}_"
                f"{safe_event_name}_"
                f"{event_time:.2f}s.mp4"
            )
        )


        # --------------------------------------------------
        # WRITE VIDEO
        # --------------------------------------------------

        print(
            "Writing video..."
        )

        clip.write_videofile(
            str(output_path),
            codec="libx264",
            audio=False,
            logger="bar"
        )


        # --------------------------------------------------
        # CLOSE CLIPS
        # --------------------------------------------------

        clip.close()
        video.close()


        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        print(
            "Saved:",
            output_path.name
        )


        return output_path