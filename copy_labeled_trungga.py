from pathlib import Path
import random
import shutil

IMAGE_DIR = Path("TraiCay640x640/CaRot")
LABEL_DIR = Path("Label/CaRot")
OUT_DIR = Path("TraiCay640x640_OK")

VALID_RATIO = 0.2
SEED = 42
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main():
    pairs = []
    skipped = []

    for image_path in IMAGE_DIR.iterdir():
        if image_path.suffix.lower() not in IMAGE_EXTS:
            continue

        label_path = LABEL_DIR / f"{image_path.stem}.txt"
        if label_path.exists():
            pairs.append((image_path, label_path))
        else:
            skipped.append(image_path.name)

    random.Random(SEED).shuffle(pairs)
    valid_count = round(len(pairs) * VALID_RATIO)
    valid_pairs = pairs[:valid_count]
    train_pairs = pairs[valid_count:]

    copy_pairs(train_pairs, "train")
    copy_pairs(valid_pairs, "valid")

    print(f"Copied train: {len(train_pairs)}")
    print(f"Copied valid: {len(valid_pairs)}")
    print(f"Skipped images without txt: {len(skipped)}")


def copy_pairs(pairs, split):
    image_out = OUT_DIR / split / "images"
    label_out = OUT_DIR / split / "labels"
    image_out.mkdir(parents=True, exist_ok=True)
    label_out.mkdir(parents=True, exist_ok=True)

    for image_path, label_path in pairs:
        shutil.copy2(image_path, image_out / image_path.name)
        shutil.copy2(label_path, label_out / label_path.name)


if __name__ == "__main__":
    main()
