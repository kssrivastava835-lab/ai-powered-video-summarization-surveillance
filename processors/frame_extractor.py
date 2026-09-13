import cv2

from configs.config import FRAME_FOLDER


class FrameExtractor:

    def __init__(self, video_path, sample_rate):

        self.video_path = str(video_path)

        self.sample_rate = sample_rate

    def extract_frames(self):

        FRAME_FOLDER.mkdir(exist_ok=True)

        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():

            raise Exception("Cannot open video.")

        fps = cap.get(cv2.CAP_PROP_FPS)

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        duration = total_frames / fps

        print("=" * 50)
        print("VIDEO INFORMATION")
        print("=" * 50)
        print(f"FPS           : {fps:.2f}")
        print(f"Resolution    : {width} x {height}")
        print(f"Total Frames  : {total_frames}")
        print(f"Duration      : {duration:.2f} seconds")
        print("=" * 50)

        frame_number = 0

        saved = 0

        while True:

            success, frame = cap.read()

            if not success:

                break

            if frame_number % self.sample_rate == 0:

                filename = FRAME_FOLDER / f"frame_{saved:05d}.jpg"

                cv2.imwrite(str(filename), frame)

                saved += 1

            frame_number += 1

        cap.release()

        print(f"\nFrames Saved : {saved}")