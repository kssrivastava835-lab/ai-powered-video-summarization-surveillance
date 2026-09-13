import json

from pathlib import Path

from ultralytics import YOLO

from configs.config import (
    MOTION_FOLDER,
    DETECTIONS_FOLDER
)


class ObjectDetector:

    def __init__(
        self,
        model_name="yolo11n.pt"
    ):

        # ==========================================
        # CREATE OUTPUT FOLDER
        # ==========================================

        DETECTIONS_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================
        # LOAD YOLO MODEL
        # ==========================================

        print(
            f"Loading YOLO model: {model_name}"
        )

        self.model = YOLO(
            model_name
        )


    def detect_objects(self):

        # ==========================================
        # FIND MOTION FRAMES
        # ==========================================

        motion_frames = sorted(
            MOTION_FOLDER.glob("*.jpg")
        )

        print(
            "Frames found:",
            len(motion_frames)
        )

        total_detections = 0
        processed_frames = 0


        # ==========================================
        # PROCESS EACH MOTION FRAME
        # ==========================================

        for image_path in motion_frames:

            print()
            print(
                "Processing:",
                image_path.name
            )


            # ======================================
            # READ TIMESTAMP METADATA
            # ======================================

            metadata_path = (
                MOTION_FOLDER
                / f"{image_path.stem}.json"
            )

            original_frame = None
            timestamp = None

            if metadata_path.exists():

                with open(
                    metadata_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    metadata = json.load(
                        file
                    )

                original_frame = metadata.get(
                    "original_frame"
                )

                timestamp = metadata.get(
                    "timestamp"
                )


            # ======================================
            # RUN YOLO
            # ======================================

            results = self.model(
                str(image_path),
                verbose=False
            )


            detections = []


            # ======================================
            # EXTRACT DETECTIONS
            # ======================================

            for result in results:

                if result.boxes is None:
                    continue

                for box in result.boxes:

                    class_id = int(
                        box.cls[0]
                    )

                    confidence = float(
                        box.conf[0]
                    )

                    bbox = (
                        box.xyxy[0]
                        .tolist()
                    )

                    class_name = (
                        self.model.names[
                            class_id
                        ]
                    )


                    detections.append({

                        "class": class_name,

                        "confidence": round(
                            confidence,
                            3
                        ),

                        "bbox": [
                            round(
                                coordinate,
                                2
                            )
                            for coordinate
                            in bbox
                        ]

                    })


            # ======================================
            # SAVE DETECTION DATA
            # ======================================

            output_data = {

                "source": image_path.name,

                "original_frame": (
                    original_frame
                ),

                "timestamp": (
                    timestamp
                ),

                "detections": detections

            }


            output_path = (
                DETECTIONS_FOLDER
                / f"{image_path.stem}.json"
            )


            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    output_data,
                    file,
                    indent=4
                )


            # ======================================
            # STATISTICS
            # ======================================

            print(
                "Detections:",
                len(detections)
            )

            if timestamp is not None:

                print(
                    "Timestamp:",
                    f"{timestamp:.3f}s"
                )

            total_detections += len(
                detections
            )

            processed_frames += 1


        # ==========================================
        # FINAL OUTPUT
        # ==========================================

        print()
        print("=" * 50)

        print(
            "Total detections:",
            total_detections
        )

        print(
            "Frames processed:",
            processed_frames
        )

        print("=" * 50)

        return total_detections