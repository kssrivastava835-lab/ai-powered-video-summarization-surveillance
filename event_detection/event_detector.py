class EventDetector:

    def __init__(self):
        # Previous state of the scene
        self.previous_person_count = 0
        self.previous_vehicle_count = 0

        # Prevent repeated events caused by small detection fluctuations
        self.last_event_time = {
            "person": -999,
            "vehicle": -999
        }

        # Minimum time between similar events
        self.event_cooldown = 3.0

    def detect_events(self, tracked_objects, timestamp=0.0):

        events = []

        person_count = 0
        vehicle_count = 0

        # --------------------------------------------------
        # 1. COUNT MEANINGFUL OBJECTS
        # --------------------------------------------------

        vehicle_classes = {
            "car",
            "truck",
            "bus",
            "motorcycle",
            "motorbike"
        }

        for track_id, obj in tracked_objects.items():

            object_class = str(
                obj.get("class", "Unknown")
            ).lower().strip()

            if object_class == "person":

                person_count += 1

            elif object_class in vehicle_classes:

                vehicle_count += 1

        # --------------------------------------------------
        # 2. PERSON APPEARED
        # --------------------------------------------------

        if person_count > self.previous_person_count:

            if (
                timestamp - self.last_event_time["person"]
                >= self.event_cooldown
            ):

                events.append({
                    "event": "Person Appeared",
                    "class": "person",
                    "count": person_count,
                    "timestamp": round(timestamp, 2)
                })

                self.last_event_time["person"] = timestamp

        # --------------------------------------------------
        # 3. VEHICLE APPEARED
        # --------------------------------------------------

        if vehicle_count > self.previous_vehicle_count:

            if (
                timestamp - self.last_event_time["vehicle"]
                >= self.event_cooldown
            ):

                events.append({
                    "event": "Vehicle Appeared",
                    "class": "vehicle",
                    "count": vehicle_count,
                    "timestamp": round(timestamp, 2)
                })

                self.last_event_time["vehicle"] = timestamp

        # --------------------------------------------------
        # 4. PERSON DISAPPEARED
        # --------------------------------------------------

        if (
            self.previous_person_count > 0
            and person_count == 0
        ):

            if (
                timestamp - self.last_event_time["person"]
                >= self.event_cooldown
            ):

                events.append({
                    "event": "Person Disappeared",
                    "class": "person",
                    "count": 0,
                    "timestamp": round(timestamp, 2)
                })

                self.last_event_time["person"] = timestamp

        # --------------------------------------------------
        # 5. VEHICLE DISAPPEARED
        # --------------------------------------------------

        if (
            self.previous_vehicle_count > 0
            and vehicle_count == 0
        ):

            if (
                timestamp - self.last_event_time["vehicle"]
                >= self.event_cooldown
            ):

                events.append({
                    "event": "Vehicle Disappeared",
                    "class": "vehicle",
                    "count": 0,
                    "timestamp": round(timestamp, 2)
                })

                self.last_event_time["vehicle"] = timestamp

        # --------------------------------------------------
        # 6. SAVE CURRENT SCENE STATE
        # --------------------------------------------------

        self.previous_person_count = person_count
        self.previous_vehicle_count = vehicle_count

        return events