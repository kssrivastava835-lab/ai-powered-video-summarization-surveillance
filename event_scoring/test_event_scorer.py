from event_scorer import EventScorer
scorer = EventScorer()
events = [
    
    {
        "event": "Vehicle Appeared",
        "track_id":0,
        "class":"Car"
    },

    {
        "event": "Person Appeared",
        "track_id":1,
        "class":"Person"
    },

    {
        "event": "Fire Detected",
        "track_id":-1,
        "class":"Fire"
    },

    {
        "event": "Dog Appeared",
        "track_id":2,
        "class":"Dog"
    },
   
]

scored = scorer.score_events(events)

important = scorer.filter_events(scored)
print("\nIMPORTANT EVENTS")

for event in important:
    print(event)

for event in scored:
    print(event)