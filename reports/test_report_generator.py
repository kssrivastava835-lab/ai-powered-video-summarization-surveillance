from report_generator import ReportGenerator
generator = ReportGenerator()

events = [
    {
        "time" : 5,
        "event": "Vehicle Appeared",
        "track_id":0,
        "class":"Car",
        "score": 40
    },

    {
        "time": 12,
        "event": "Person Appeared",
        "track_id": 1,
        "class": "Person",
        "score": 60
    },

    {
        "time":20,
        "event":"Fire Detected",
        "track_id":-1,
        "class":"Fire",
        "score":100
    }
]

print("=" * 50)
print("INPUT EVENTS")
print("=" * 50)

for event in events:
    print(event)

report_path = generator.generate_report(events)

print()
print("=" * 50)
print("FINAL REPORT")
print("=" * 50)

