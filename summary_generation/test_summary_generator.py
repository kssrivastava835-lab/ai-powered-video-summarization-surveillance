from pathlib import Path
from summary_generation.summary_generator import SummaryGenerator
generator = SummaryGenerator()

clips_folder = Path("clips")
clip_paths = sorted(
    clips_folder.glob("*.mp4")
)


print("=" * 50)
print("CLIPS FOUND")
print("="*50)

for clip in clip_paths: 
    print(clip)

print("\n")
summary_path = generator.create_summary(
    clip_paths
)

print("\n")
print("=" * 50)
print("FINAL OUTPUT")
print("=" * 50)

print(summary_path)
