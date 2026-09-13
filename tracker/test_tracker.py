from object_tracker import CentroidTracker

# Create tracker object
tracker = CentroidTracker()

frame1 = [
    {
        "class": "Car",
        "confidence": 0.95,
        "bbox": [100,100,200,200]
    },
    {
        "class": "Person",
        "confidence": 0.91,
        "bbox": [500,100,560,250]
    }
]

frame2 = [
    {
        "class": "Car",
        "confidence": 0.94,
        "bbox": [110,105,210,205]
    },
    {
        "class": "Person",
        "confidence": 0.92,
        "bbox": [510,110,570,260]
    }
]

print("\nFRAME 1")
print(tracker.update(frame1))

print("\nFRAME 2")
print(tracker.update(frame2))

