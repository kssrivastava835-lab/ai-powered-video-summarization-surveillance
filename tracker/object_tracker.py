from math import hypot


class CentroidTracker:

    def __init__(
        self,
        max_distance=80,
        max_disappeared=5
    ):

        self.next_object_id = 0

        self.objects = {}

        # How far an object can move between frames
        self.max_distance = max_distance

        # Number of consecutive frames an object
        # can disappear before we remove it
        self.max_disappeared = max_disappeared

        self.disappeared = {}

    def _centroid(self, bbox):

        xmin, ymin, xmax, ymax = bbox

        cx = int((xmin + xmax) / 2)
        cy = int((ymin + ymax) / 2)

        return (cx, cy)

    def update(self, detections):

        tracked_objects = {}

        # --------------------------------------------------
        # CASE 1: No existing objects
        # --------------------------------------------------

        if len(self.objects) == 0:

            for detection in detections:

                object_id = self.next_object_id

                centroid = self._centroid(
                    detection["bbox"]
                )

                self.objects[object_id] = {
                    "centroid": centroid,
                    "class": detection["class"],
                    "bbox": detection["bbox"]
                }

                self.disappeared[object_id] = 0

                detection["track_id"] = object_id

                tracked_objects[object_id] = detection

                self.next_object_id += 1

            return tracked_objects

        # --------------------------------------------------
        # CASE 2: No detections in current frame
        # --------------------------------------------------

        if len(detections) == 0:

            for object_id in list(self.objects.keys()):

                self.disappeared[object_id] += 1

                if (
                    self.disappeared[object_id]
                    > self.max_disappeared
                ):

                    del self.objects[object_id]
                    del self.disappeared[object_id]

            return tracked_objects

        # --------------------------------------------------
        # Calculate current centroids
        # --------------------------------------------------

        input_centroids = []

        for detection in detections:

            centroid = self._centroid(
                detection["bbox"]
            )

            input_centroids.append(
                centroid
            )

        object_ids = list(
            self.objects.keys()
        )

        object_centroids = [
            self.objects[obj_id]["centroid"]
            for obj_id in object_ids
        ]

        # --------------------------------------------------
        # Match detections with existing objects
        # --------------------------------------------------

        used_object_ids = set()
        used_detection_indexes = set()

        matches = []

        for detection_index, centroid in enumerate(
            input_centroids
        ):

            best_id = None
            best_distance = float("inf")

            for object_index, object_id in enumerate(
                object_ids
            ):

                if object_id in used_object_ids:
                    continue

                old_centroid = object_centroids[
                    object_index
                ]

                distance = hypot(
                    centroid[0] - old_centroid[0],
                    centroid[1] - old_centroid[1]
                )

                if (
                    distance < best_distance
                    and distance <= self.max_distance
                ):

                    best_distance = distance
                    best_id = object_id

            if best_id is not None:

                matches.append(
                    (
                        best_id,
                        detection_index
                    )
                )

                used_object_ids.add(
                    best_id
                )

                used_detection_indexes.add(
                    detection_index
                )

        # --------------------------------------------------
        # Update matched objects
        # --------------------------------------------------

        for object_id, detection_index in matches:

            detection = detections[
                detection_index
            ]

            centroid = input_centroids[
                detection_index
            ]

            self.objects[object_id] = {
                "centroid": centroid,
                "class": detection["class"],
                "bbox": detection["bbox"]
            }

            self.disappeared[object_id] = 0

            detection["track_id"] = object_id

            tracked_objects[
                object_id
            ] = detection

        # --------------------------------------------------
        # Handle unmatched existing objects
        # --------------------------------------------------

        for object_id in object_ids:

            if object_id not in used_object_ids:

                self.disappeared[object_id] += 1

                if (
                    self.disappeared[object_id]
                    > self.max_disappeared
                ):

                    del self.objects[
                        object_id
                    ]

                    del self.disappeared[
                        object_id
                    ]

        # --------------------------------------------------
        # Register NEW objects
        # --------------------------------------------------

        for detection_index, detection in enumerate(
            detections
        ):

            if (
                detection_index
                in used_detection_indexes
            ):
                continue

            centroid = input_centroids[
                detection_index
            ]

            object_id = self.next_object_id

            self.objects[object_id] = {
                "centroid": centroid,
                "class": detection["class"],
                "bbox": detection["bbox"]
            }

            self.disappeared[object_id] = 0

            detection["track_id"] = object_id

            tracked_objects[
                object_id
            ] = detection

            self.next_object_id += 1

        return tracked_objects