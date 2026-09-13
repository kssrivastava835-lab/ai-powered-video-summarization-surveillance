from pathlib import Path
import json


class TimelineGenerator:

    def __init__(self, output_folder="output"):

        self.output_folder = Path(
            output_folder
        )

        self.timeline_folder = (
            self.output_folder / "timeline"
        )

        self.timeline_folder.mkdir(
            parents=True,
            exist_ok=True
        )


    def generate_timeline(self, events):

        # --------------------------------------------------
        # CHECK EVENTS
        # --------------------------------------------------

        if not events:

            raise ValueError(
                "No events available for timeline."
            )


        # --------------------------------------------------
        # SORT EVENTS BY TIMESTAMP
        # --------------------------------------------------

        sorted_events = sorted(
            events,
            key=lambda event: event.get(
                "timestamp",
                0.0
            )
        )


        # --------------------------------------------------
        # CREATE TIMELINE
        # --------------------------------------------------

        timeline = []

        for index, event in enumerate(
            sorted_events,
            start=1
        ):

            timeline_event = {
                "event_id": index,
                "timestamp": event.get(
                    "timestamp",
                    0.0
                ),
                "event": event.get(
                    "event",
                    "Unknown Event"
                ),
                "class": event.get(
                    "class",
                    "Unknown"
                ),
                "count": event.get(
                    "count",
                    0
                )
            }

            timeline.append(
                timeline_event
            )


        # --------------------------------------------------
        # CREATE OUTPUT
        # --------------------------------------------------

        timeline_data = {
            "total_events": len(timeline),
            "events": timeline
        }


        # --------------------------------------------------
        # SAVE JSON
        # --------------------------------------------------

        output_path = (
            self.timeline_folder
            / "timeline.json"
        )


        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                timeline_data,
                file,
                indent=4
            )


        # --------------------------------------------------
        # PRINT RESULT
        # --------------------------------------------------

        print()
        print(
            "Timeline generated successfully!"
        )

        print(
            "Total timeline events:",
            len(timeline)
        )

        print(
            "Saved:",
            output_path
        )


        return output_path