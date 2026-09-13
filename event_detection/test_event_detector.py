from event_detector import EventDetector
detector = EventDetector()

# Frame 1

frame1 = {
    0:{
        "track_id":0,
        "class":"Car"
    }
}

# Frame 2
frame2 = {
    0:{
        "track_id": 0,
        "class":"Car"  
    },
    1: {
        "track_id" : 1,
        "class":"Person"
    }
}

# Frame 3
frame3 = {
    1:{
        "track_id":1,
        "class":"Person"
    }
}

# Frame 4
frame4 = {
    1: {
        "track_id" : 1,
        "class": "Person"
    },
    2: {
        "track_id" : 2 ,
        "class" : "Truck"
    }
}

print("\nFRAME 1")
print(detector.detect_events(frame1))

print("\nFRAME 2")
print(detector.detect_events(frame2))

print("\nFRAME 3")
print(detector.detect_events(frame3))

print("\nFRAME 4")
print(detector.detect_events(frame4))