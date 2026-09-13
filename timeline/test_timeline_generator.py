from timeline.timeline_generator import TimelineGenerator
generator = TimelineGenerator()

events = [
    {
        "time" : 5,
        "event" : "Vehicle Appeared",
        "track_id":0,
        "class":"Car",
        "score":40
    },

    {
        "time" : 12,
        "event" : "Person Appeared",
        "track_id":1,
        "class":"Person",
        "score":60
    },

    {
        "time" : 20,
        "event" : "Fire Appeared",
        "track_id":-1,
        "class":"Fire",
        "score":100
    },

    {
        "time" : 8,
        "event" : "Dog Appeared",
        "track_id":2,
        "class":"Dog",
        "score":20
    },
    
]

print("=" * 50)
print("INPUT EVENTS")
print("=" * 50)

for event in events:
    print(event)

timeline = generator.generate_timeline(events)

print()
print("=" * 50)
print("GENERATED TIMELINE")
print("=" * 50)

for event in timeline:
    print(event)

  