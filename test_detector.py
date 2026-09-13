from pathlib import Path
from models.object_detector import ObjectDetector


def main():

    print("=" * 60)
    print("TensorFlow Object Detection Test")
    print("=" * 60)

    # Create detector
    detector = ObjectDetector()

    # Test image
    image_path = Path("motion_frames/motion_00000.jpg")

    # Check image exists
    if not image_path.exists():
        print(f"\nImage not found: {image_path}")
        return

    print(f"\nProcessing Image : {image_path.name}")

    # Run detection
    image, outputs = detector.detect(image_path)

    # -----------------------------
    # Print model information
    # -----------------------------
    print("\n" + "=" * 60)
    print("MODEL OUTPUT INFORMATION")
    print("=" * 60)

    print("\nAvailable Keys:")
    print(outputs.keys())

    print("\nTensor Shapes:")
    for key, value in outputs.items():
        print(f"{key:30} {value.shape}")

    # -----------------------------
    # Print first 10 detections
    # -----------------------------
    print("\n" + "=" * 60)
    print("TOP 10 MODEL PREDICTIONS")
    print("=" * 60)

    print("\nLabels:")
    print(outputs["detection_class_labels"][:10].numpy())

    print("\nEntities:")
    print(outputs["detection_class_entities"][:10].numpy())

    print("\nNames:")
    print(outputs["detection_class_names"][:10].numpy())

    print("\nScores:")
    print(outputs["detection_scores"][:10].numpy())

    # -----------------------------
    # Draw boxes
    # -----------------------------
    detections = detector.draw_boxes(
        image,
        outputs,
        image_path.name
    )

    # -----------------------------
    # Save JSON
    # -----------------------------
    detector.save_json(
        image_path.name,
        detections
    )

    # -----------------------------
    # Final Results
    # -----------------------------
    print("\n" + "=" * 60)
    print("FINAL DETECTIONS")
    print("=" * 60)

    if len(detections) == 0:
        print("\nNo objects detected with confidence >= 0.50")

    else:
        for i, detection in enumerate(detections, start=1):
            print(f"\nDetection {i}")
            print(f"Class      : {detection['class']}")
            print(f"Confidence : {detection['confidence']:.2f}")
            print(f"BBox       : {detection['bbox']}")

    print("\n" + "=" * 60)
    print("Detection Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()