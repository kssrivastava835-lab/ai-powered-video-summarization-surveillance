from pathlib import Path
import json


class ReportGenerator:

    def __init__(self, output_folder="output"):

        self.output_folder = Path(output_folder)

        self.report_folder = (
            self.output_folder / "reports"
        )

        self.report_folder.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_report(self, events):

        if not events:
            raise ValueError(
                "No events available for report."
            )

        total_events = len(events)

        person_events = 0
        vehicle_events = 0

        vehicle_classes = {
            "car",
            "truck",
            "bus",
            "motorcycle",
            "motorbike",
            "vehicle"
        }

        for event in events:

            event_class = str(
                event.get(
                    "class",
                    ""
                )
            ).strip().lower()

            if event_class == "person":

                person_events += 1

            elif event_class in vehicle_classes:

                vehicle_events += 1

        report = {

            "project":
                "AI Video Summarization for Surveillance",

            "total_events":
                total_events,

            "person_events":
                person_events,

            "vehicle_events":
                vehicle_events,

            "events":
                events
        }

        output_path = (
            self.report_folder
            / "surveillance_report.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4
            )

        print()
        print(
            "Report Generated"
        )

        print(
            "Total Events:",
            total_events
        )

        print(
            "Person Events:",
            person_events
        )

        print(
            "Vehicle Events:",
            vehicle_events
        )

        print(
            "Saved:",
            output_path
        )

        return output_path