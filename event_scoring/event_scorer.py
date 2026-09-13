class EventScorer:
    def __init__(self):
        self.score_table = {
            "Fire Detected":100,
            "Fight Detected":95,
            "Fall Detected":90,
            "Unknown Person": 85,
            "Person Appeared":60,
            "Person Disappeared":55,
            "Vehicle Appeared":40,
            "Vehicle Disappeared":35,
            "Dog Appeared":20,
            "Cat Appeared":20
        }

    def score_events(self,events):
        scored_events = []
        for event in events:
            score =  self.score_table.get(
                event["event"],
                10
            )

            event["score"] = score
            scored_events.append(event)

        return scored_events

    def filter_events(
        self,
        scored_events,
        threshold=50
        ):

        important = []

        for event in scored_events:

            if event["score"] >= threshold:

                important.append(event)

        return important