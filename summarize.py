'''"""
Main entry point for the project.
"""

from utils.helpers import create_folders
from utils.logger import setup_logger


def main():

    create_folders()

    logger = setup_logger()

    logger.info("====================================")
    logger.info("AI Video Summarizer Started")
    logger.info("Project initialized successfully.")
    logger.info("====================================")


if __name__ == "__main__":
    main() '''

'''from configs.config import VIDEO_FOLDER
from configs.config import FRAME_SAMPLE_RATE

from processors.frame_extractor import FrameExtractor
from detectors.motion_detector import MotionDetector


def main():

    video_path = VIDEO_FOLDER / "sample.mp4"
    print("Video Path:",video_path)
    extractor = FrameExtractor(
        video_path=video_path,
        sample_rate=FRAME_SAMPLE_RATE
    )
    extractor.extract_frames()

    detector = MotionDetector()
    detector.detect_motion(video_path)


if __name__ == "__main__":
    main()'''

