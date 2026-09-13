import cv2
import json

from configs.config import (
    MOTION_FOLDER,
    MOTION_THRESHOLD,
    MIN_CONTOUR_AREA
)


class MotionDetector:

    def __init__(self, save_every_n_motion_frames=5):

        MOTION_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        self.save_every_n_motion_frames = (
            save_every_n_motion_frames
        )

    def detect_motion(self, video_path):

        cap = cv2.VideoCapture(
            str(video_path)
        )

        if not cap.isOpened():
            raise Exception(
                "Unable to open video."
            )

        # Get actual FPS
        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        if fps <= 0:
            fps = 30.0

        ret, previous_frame = cap.read()

        if not ret:
            cap.release()
            raise Exception(
                "Unable to read video."
            )

        previous_gray = cv2.cvtColor(
            previous_frame,
            cv2.COLOR_BGR2GRAY
        )

        previous_gray = cv2.GaussianBlur(
            previous_gray,
            (21, 21),
            0
        )

        frame_number = 1
        saved = 0
        motion_frame_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            gray = cv2.GaussianBlur(
                gray,
                (21, 21),
                0
            )

            difference = cv2.absdiff(
                previous_gray,
                gray
            )

            _, threshold = cv2.threshold(
                difference,
                MOTION_THRESHOLD,
                255,
                cv2.THRESH_BINARY
            )

            threshold = cv2.dilate(
                threshold,
                None,
                iterations=2
            )

            contours, _ = cv2.findContours(
                threshold,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            motion_detected = False

            for contour in contours:

                if cv2.contourArea(
                    contour
                ) < MIN_CONTOUR_AREA:
                    continue

                motion_detected = True

                x, y, w, h = cv2.boundingRect(
                    contour
                )

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

            # ==========================================
            # MOTION FRAME SAMPLING
            # ==========================================

            if motion_detected:

                motion_frame_count += 1

                if (
                    motion_frame_count
                    % self.save_every_n_motion_frames
                    == 0
                ):

                    filename = (
                        MOTION_FOLDER
                        / f"motion_{saved:05d}.jpg"
                    )

                    cv2.imwrite(
                        str(filename),
                        frame
                    )

                    # ==================================
                    # REAL TIMESTAMP
                    # ==================================

                    timestamp = (
                        frame_number / fps
                    )

                    metadata = {
                        "motion_frame": filename.name,
                        "original_frame": frame_number,
                        "timestamp": round(
                            timestamp,
                            3
                        )
                    }

                    # ==================================
                    # SAVE METADATA JSON
                    # ==================================

                    metadata_path = (
                        MOTION_FOLDER
                        / f"motion_{saved:05d}.json"
                    )

                    with open(
                        metadata_path,
                        "w",
                        encoding="utf-8"
                    ) as file:

                        json.dump(
                            metadata,
                            file,
                            indent=4
                        )

                    saved += 1

            previous_gray = gray
            frame_number += 1

        cap.release()

        print(
            "Motion frames detected:",
            motion_frame_count
        )

        print(
            "Motion Frames Saved:",
            saved
        )

        print(
            "Video FPS:",
            fps
        )

        return saved