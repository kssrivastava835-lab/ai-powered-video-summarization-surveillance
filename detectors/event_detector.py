class EventDetector:

    def __init__(self, min_presence_frames=2):
        self.min_presence_frames = min_presence_frames

        # How many consecutive frames each object has been seen
        self.presence_count = {}

        # Objects that have already generated an "Appeared" event
        self.active_ids = set()

        # Remember the class of each tracked object
        self.object_classes = {}

        # Number of consecutive frames an object has been missing
        self.missing_count = {}

        # Don't immediately declare an object disappeared
        self.max_missing_frames = 2

    def detect_events(self, tracked_objects, timestamp=0.0):

        events = []

        # Only consider meaningful surveillance objects
        allowed_classes = {
            "person",
            "car",
            "truck",
            "bus",
            "motorcycle",
            "motorbike"
        }

        current_objects = {}

        # --------------------------------------------------
        # 1. FILTER OBJECTS
        # --------------------------------------------------

        for track_id, obj in tracked_objects.items():

            object_class = str(
                obj.get("class", "Unknown")
            ).lower().strip()

            if object_class not in allowed_classes:
                continue

            current_objects[track_id] = obj

            self.object_classes[track_id] = object_class

            # Object is currently visible
            self.missing_count[track_id] = 0

        current_ids = set(current_objects.keys())

        # --------------------------------------------------
        # 2. COUNT OBJECT PRESENCE
        # --------------------------------------------------

        for track_id in current_ids:

            self.presence_count[track_id] = (
                self.presence_count.get(track_id, 0) + 1
            )

        # --------------------------------------------------
        # 3. DETECT NEW OBJECTS
        # --------------------------------------------------

        for track_id in current_ids:

            # Already active → don't create another event
            if track_id in self.active_ids:
                continue

            # Require object to be visible more than once
            if (
                self.presence_count[track_id]
                < self.min_presence_frames
            ):
                continue

            object_class = self.object_classes[track_id]

            if object_class == "person":
                event_name = "Person Appeared"
            else:
                event_name = "Vehicle Appeared"

            events.append({
                "event": event_name,
                "track_id": track_id,
                "class": object_class,
                "timestamp": round(timestamp, 2)
            })

            self.active_ids.add(track_id)

        # --------------------------------------------------
        # 4. HANDLE MISSING OBJECTS
        # --------------------------------------------------

        for track_id in list(self.active_ids):

            if track_id in current_ids:
                continue

            # Object was not detected in this frame
            self.missing_count[track_id] = (
                self.missing_count.get(track_id, 0) + 1
            )

            # Don't immediately call it disappeared
            if (
                self.missing_count[track_id]
                < self.max_missing_frames
            ):
                continue

            object_class = self.object_classes.get(
                track_id,
                "Unknown"
            )

            if object_class == "person":

                event_name = "Person Disappeared"

            elif object_class in {
                "car",
                "truck",
                "bus",
                "motorcycle",
                "motorbike"
            }:

                event_name = "Vehicle Disappeared"

            else:
                continue

            events.append({
                "event": event_name,
                "track_id": track_id,
                "class": object_class,
                "timestamp": round(timestamp, 2)
            })

            # Remove from active tracking
            self.active_ids.remove(track_id)

            self.presence_count.pop(
                track_id,
                None
            )

            self.missing_count.pop(
                track_id,
                None
            )

            self.object_classes.pop(
                track_id,
                None
            )

        return events