import json
from pathlib import Path

import cv2
import numpy as np
import onnxruntime as ort

from configs.config import (
    MOTION_FOLDER,
    DETECTIONS_FOLDER
)


class ObjectDetector:

    # ==========================================
    # COCO CLASS NAMES
    # ==========================================

    CLASS_NAMES = [
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "dining table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush"
    ]

    def __init__(
        self,
        model_name="yolo11n.onnx"
    ):

        # ==========================================
        # CREATE OUTPUT FOLDER
        # ==========================================

        DETECTIONS_FOLDER.mkdir(
            parents=True,
            exist_ok=True
        )

        # ==========================================
        # FIND ONNX MODEL
        # ==========================================

        model_path = (
            Path(__file__).resolve().parent.parent
            / model_name
        )

        if not model_path.exists():

            raise FileNotFoundError(
                f"ONNX model not found: "
                f"{model_path}"
            )

        print()
        print(
            "Loading ONNX model:",
            model_path
        )

        # ==========================================
        # CREATE ONNX SESSION
        # ==========================================

        self.session = ort.InferenceSession(
            str(model_path),
            providers=["CPUExecutionProvider"]
        )

        self.input_name = (
            self.session.get_inputs()[0].name
        )

        self.output_name = (
            self.session.get_outputs()[0].name
        )

        input_shape = (
            self.session.get_inputs()[0].shape
        )

        print(
            "ONNX model loaded successfully"
        )

        print(
            "Input name:",
            self.input_name
        )

        print(
            "Input shape:",
            input_shape
        )

        print(
            "Output name:",
            self.output_name
        )


    # ==========================================
    # LETTERBOX
    # ==========================================

    def letterbox(
        self,
        image,
        new_shape=(320, 320)
    ):

        height, width = image.shape[:2]

        new_height, new_width = new_shape

        scale = min(
            new_width / width,
            new_height / height
        )

        resized_width = int(
            round(width * scale)
        )

        resized_height = int(
            round(height * scale)
        )

        resized = cv2.resize(
            image,
            (
                resized_width,
                resized_height
            ),
            interpolation=cv2.INTER_LINEAR
        )

        pad_width = new_width - resized_width
        pad_height = new_height - resized_height

        left = pad_width // 2
        right = pad_width - left

        top = pad_height // 2
        bottom = pad_height - top

        padded = cv2.copyMakeBorder(
            resized,
            top,
            bottom,
            left,
            right,
            cv2.BORDER_CONSTANT,
            value=(114, 114, 114)
        )

        return (
            padded,
            scale,
            left,
            top
        )


    # ==========================================
    # PREPROCESS IMAGE
    # ==========================================

    def preprocess(
        self,
        image
    ):

        image, scale, pad_x, pad_y = (
            self.letterbox(
                image,
                (320, 320)
            )
        )

        # BGR → RGB

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        # uint8 → float32

        image = image.astype(
            np.float32
        )

        # Normalize 0-255 → 0-1

        image /= 255.0

        # HWC → CHW

        image = np.transpose(
            image,
            (2, 0, 1)
        )

        # Add batch dimension

        image = np.expand_dims(
            image,
            axis=0
        )

        return (
            image,
            scale,
            pad_x,
            pad_y
        )


    # ==========================================
    # IOU
    # ==========================================

    def calculate_iou(
        self,
        box1,
        box2
    ):

        x1 = max(
            box1[0],
            box2[0]
        )

        y1 = max(
            box1[1],
            box2[1]
        )

        x2 = min(
            box1[2],
            box2[2]
        )

        y2 = min(
            box1[3],
            box2[3]
        )

        intersection_width = max(
            0,
            x2 - x1
        )

        intersection_height = max(
            0,
            y2 - y1
        )

        intersection = (
            intersection_width
            * intersection_height
        )

        area1 = (
            max(
                0,
                box1[2] - box1[0]
            )
            *
            max(
                0,
                box1[3] - box1[1]
            )
        )

        area2 = (
            max(
                0,
                box2[2] - box2[0]
            )
            *
            max(
                0,
                box2[3] - box2[1]
            )
        )

        union = (
            area1
            + area2
            - intersection
        )

        if union <= 0:
            return 0.0

        return intersection / union


    # ==========================================
    # NMS
    # ==========================================

    def nms(
        self,
        boxes,
        scores,
        iou_threshold=0.45
    ):

        if not boxes:
            return []

        indices = np.argsort(
            scores
        )[::-1]

        keep = []

        while len(indices) > 0:

            current = indices[0]

            keep.append(
                current
            )

            remaining = []

            for index in indices[1:]:

                iou = self.calculate_iou(
                    boxes[current],
                    boxes[index]
                )

                if iou < iou_threshold:

                    remaining.append(
                        index
                    )

            indices = np.array(
                remaining,
                dtype=np.int64
            )

        return keep


    # ==========================================
    # DETECT ONE IMAGE
    # ==========================================

    def detect_image(
        self,
        image_path
    ):

        image = cv2.imread(
            str(image_path)
        )

        if image is None:

            print(
                "Unable to read:",
                image_path
            )

            return []


        original_height, original_width = (
            image.shape[:2]
        )


        # ======================================
        # PREPROCESS
        # ======================================

        input_tensor, scale, pad_x, pad_y = (
            self.preprocess(image)
        )


        # ======================================
        # ONNX INFERENCE
        # ======================================

        outputs = self.session.run(
            [self.output_name],
            {
                self.input_name:
                input_tensor
            }
        )


        predictions = outputs[0]


        # ======================================
        # REMOVE BATCH DIMENSION
        # ======================================

        predictions = np.squeeze(
            predictions
        )


        # YOLO output can be:
        #
        # (84, 8400)
        #
        # or
        #
        # (8400, 84)
        #
        # Convert to:
        #
        # (8400, 84)

        if predictions.shape[0] < predictions.shape[1]:

            predictions = predictions.T


        boxes = []
        scores = []
        class_ids = []


        # ======================================
        # PROCESS PREDICTIONS
        # ======================================

        for prediction in predictions:

            x_center = prediction[0]
            y_center = prediction[1]

            box_width = prediction[2]
            box_height = prediction[3]

            class_scores = prediction[4:]

            class_id = int(
                np.argmax(
                    class_scores
                )
            )

            confidence = float(
                class_scores[class_id]
            )

            if confidence < 0.50:
                continue


            # ==================================
            # XYWH → XYXY
            # ==================================

            x1 = (
                x_center
                - box_width / 2
            )

            y1 = (
                y_center
                - box_height / 2
            )

            x2 = (
                x_center
                + box_width / 2
            )

            y2 = (
                y_center
                + box_height / 2
            )


            # ==================================
            # REMOVE LETTERBOX PADDING
            # ==================================

            x1 = (
                x1 - pad_x
            ) / scale

            y1 = (
                y1 - pad_y
            ) / scale

            x2 = (
                x2 - pad_x
            ) / scale

            y2 = (
                y2 - pad_y
            ) / scale


            # ==================================
            # CLIP BOX TO IMAGE
            # ==================================

            x1 = max(
                0,
                min(
                    x1,
                    original_width
                )
            )

            y1 = max(
                0,
                min(
                    y1,
                    original_height
                )
            )

            x2 = max(
                0,
                min(
                    x2,
                    original_width
                )
            )

            y2 = max(
                0,
                min(
                    y2,
                    original_height
                )
            )


            boxes.append(
                [
                    x1,
                    y1,
                    x2,
                    y2
                ]
            )

            scores.append(
                confidence
            )

            class_ids.append(
                class_id
            )


        # ======================================
        # NMS
        # ======================================

        keep_indices = self.nms(
            boxes,
            scores,
            iou_threshold=0.45
        )


        detections = []


        # ======================================
        # CREATE DETECTIONS
        # ======================================

        for index in keep_indices:

            class_id = class_ids[
                index
            ]

            confidence = scores[
                index
            ]

            bbox = boxes[
                index
            ]

            if class_id >= len(
                self.CLASS_NAMES
            ):

                class_name = (
                    f"class_{class_id}"
                )

            else:

                class_name = (
                    self.CLASS_NAMES[
                        class_id
                    ]
                )


            detections.append({

                "class": str(class_name),

                "confidence": float(
                    round(
                        float(confidence),
                        3
                    )
                ),

                "bbox": [
                    float(
                        round(
                            float(coordinate),
                            2
                        )
                    )
                    for coordinate in bbox
                ]

            })
        
        return detections
        


    # ==========================================
    # DETECT ALL MOTION FRAMES
    # ==========================================

    def detect_objects(self):

        motion_frames = sorted(
            MOTION_FOLDER.glob("*.jpg")
        )

        print()
        print(
            "Frames found:",
            len(motion_frames)
        )

        total_detections = 0
        processed_frames = 0


        # ==========================================
        # PROCESS EACH FRAME
        # ==========================================

        for image_path in motion_frames:

            print()
            print(
                "Processing:",
                image_path.name
            )


            # ======================================
            # READ METADATA
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
            # RUN ONNX DETECTION
            # ======================================

            detections = self.detect_image(
                image_path
            )


            # ======================================
            # SAVE RESULT
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