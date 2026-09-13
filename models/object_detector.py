import cv2
import json
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub




from pathlib import Path
from configs.config import (
    DETECTED_FRAME_FOLDER,
    DETECTION_JSON_FOLDER,
)



class ObjectDetector:
    def __init__(self):
        DETECTED_FRAME_FOLDER.mkdir(parents= True ,exist_ok=True)
        DETECTION_JSON_FOLDER.mkdir(parents = True,exist_ok = True)

        print("=" * 50)
        print("Loading Tensorflow SSD MobileNet...")
        print("=" * 50)

        self.model = hub.load(
            "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
        )

        print("Model Loaded Successfully")
    
    def detect(self,image_path):
        image = cv2.imread(str(image_path))
        if image is None:
            raise Exception("Unable to read the image.")
        
        rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        rgb = rgb.astype(np.float32) / 255.0
        tensor = tf.convert_to_tensor(rgb,dtype = tf.float32)
        tensor = tf.expand_dims(tensor,axis = 0)
        outputs = self.model.signatures["default"](tensor)
        return image,outputs
    
    def draw_boxes(self,image,outputs,image_name):
        height , width , _ = image.shape
        boxes = outputs["detection_boxes"].numpy()
        scores = outputs["detection_scores"].numpy()
        entities = outputs["detection_class_entities"].numpy()

        detection_list = []
        for box,score,entity in zip(boxes,scores,entities):
            if score < 0.50:
                continue
        
            label = entity.decode("utf-8")
         

            ymin,xmin,ymax,xmax = box
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)

            cv2.rectangle(
                image,
                (xmin,ymin),
                (xmax,ymax),
                (0,255,0),
                2
            )

            cv2.putText(
                image,
                f"{label} {score:.2f}",
                (xmin,ymin - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

            detection_list.append({
                "class":label,
                "confidence": float(score),
                "bbox" : [
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                ]
            })

        save_path = DETECTED_FRAME_FOLDER / image_name
        cv2.imwrite(str(save_path),image)
        return detection_list

    def save_json(self,image_name,detections):
        json_path = (
            DETECTION_JSON_FOLDER /
            image_name.replace(".jpg",".json")
        )

        with open(json_path,"w") as f:
            json.dump(
                detections,
                f,
                indent= 4
            )

        print(f"JSON Saved : {json_path.name}")
    







