from pathlib import Path

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips

from configs.config import OUTPUT_FOLDER


class SummaryGenerator:

    def __init__(self):

        self.output_folder = Path(
            OUTPUT_FOLDER
        )

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
        )


    def create_summary(self, clip_paths):

        # --------------------------------------------------
        # CHECK CLIPS
        # --------------------------------------------------

        if not clip_paths:

            raise ValueError(
                "No clips available for summary."
            )


        valid_clips = []

        for clip_path in clip_paths:

            clip_path = Path(
                clip_path
            )

            if not clip_path.exists():

                print(
                    "Skipping missing clip:",
                    clip_path
                )

                continue

            valid_clips.append(
                clip_path
            )


        if not valid_clips:

            raise ValueError(
                "No valid clips found."
            )


        # --------------------------------------------------
        # LOAD CLIPS
        # --------------------------------------------------

        print()
        print(
            "Loading event clips..."
        )

        video_clips = []

        for clip_path in valid_clips:

            print(
                "Loading:",
                clip_path.name
            )

            clip = VideoFileClip(
                str(clip_path)
            )

            # Make sure summary contains no audio
            clip = clip.without_audio()

            video_clips.append(
                clip
            )


        # --------------------------------------------------
        # COMBINE CLIPS
        # --------------------------------------------------

        print()
        print(
            "Combining clips..."
        )

        summary = concatenate_videoclips(
            video_clips,
            method="compose"
        )


        # --------------------------------------------------
        # REMOVE AUDIO FROM FINAL SUMMARY
        # --------------------------------------------------

        summary = summary.without_audio()


        # --------------------------------------------------
        # OUTPUT PATH
        # --------------------------------------------------

        output_path = (
            self.output_folder
            / "summary.mp4"
        )


        # --------------------------------------------------
        # WRITE SUMMARY VIDEO
        # --------------------------------------------------

        print()
        print(
            "Creating summary video..."
        )

        summary.write_videofile(
            str(output_path),
            codec="libx264",
            audio=False,
            logger="bar"
        )


        # --------------------------------------------------
        # CLOSE RESOURCES
        # --------------------------------------------------

        summary.close()

        for clip in video_clips:

            clip.close()


        # --------------------------------------------------
        # RESULT
        # --------------------------------------------------

        print()
        print(
            "Summary created successfully!"
        )

        print(
            "Saved:",
            output_path
        )


        return output_path