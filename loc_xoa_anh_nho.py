import argparse
from pathlib import Path

from PIL import Image, UnidentifiedImageError


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_bad_image(image_path, min_width, min_height):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
    except (UnidentifiedImageError, OSError):
        return True, "loi_doc_anh"

    if width < min_width or height < min_height:
        return True, f"{width}x{height}"

    return False, f"{width}x{height}"


def delete_label_if_exists(image_path, label_dir):
    if label_dir is None:
        return None

    label_path = label_dir / f"{image_path.stem}.txt"
    if label_path.exists():
        label_path.unlink()
        return label_path

    return None


def label_path_for_image(image_path, image_dir, label_dir):
    if label_dir is None:
        return None

    relative_path = image_path.relative_to(image_dir)
    return label_dir / relative_path.with_suffix(".txt")


def rename_images(image_dir, name_prefix, label_dir=None, recursive=False):
    pattern = "**/*" if recursive else "*"
    image_paths = sorted(
        path
        for path in image_dir.glob(pattern)
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    )

    temp_items = []
    for index, image_path in enumerate(image_paths, start=1):
        label_path = label_path_for_image(image_path, image_dir, label_dir)
        temp_path = image_path.with_name(f"__rename_tmp_img_{index}{image_path.suffix.lower()}")
        temp_label_path = None

        image_path.rename(temp_path)

        if label_path is not None and label_path.exists():
            temp_label_path = label_path.with_name(f"__rename_tmp_label_{index}.txt")
            label_path.rename(temp_label_path)

        temp_items.append((temp_path, temp_label_path))

    renamed_paths = []
    for index, (temp_path, temp_label_path) in enumerate(temp_items, start=1):
        new_path = temp_path.with_name(f"{name_prefix}_{index}{temp_path.suffix.lower()}")
        temp_path.rename(new_path)

        if temp_label_path is not None:
            new_label_path = temp_label_path.with_name(f"{name_prefix}_{index}.txt")
            temp_label_path.rename(new_label_path)

        renamed_paths.append(new_path)

    return renamed_paths


def main():
    parser = argparse.ArgumentParser(
        description="Loc va xoa anh qua nho hoac anh bi loi khong the danh nhan."
    )
    parser.add_argument(
        "image_dir",
        help="Thu muc chua anh, vi du: TraiCay640x640\\CaRot",
    )
    parser.add_argument(
        "--min-width",
        type=int,
        default=100,
        help="Chieu rong toi thieu. Mac dinh: 100",
    )
    parser.add_argument(
        "--min-height",
        type=int,
        default=100,
        help="Chieu cao toi thieu. Mac dinh: 100",
    )
    parser.add_argument(
        "--label-dir",
        default=None,
        help="Thu muc label .txt tuong ung neu muon xoa kem, vi du: Label\\CaRot",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Quet ca cac thu muc con.",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Xoa that. Neu khong co tham so nay thi chi hien thi danh sach.",
    )
    parser.add_argument(
        "--rename",
        action="store_true",
        help="Sau khi xoa, doi ten tat ca anh con lai theo dang ten_1, ten_2...",
    )
    parser.add_argument(
        "--rename-prefix",
        default=None,
        help="Ten dung de doi anh. Neu bo qua se lay ten thu muc anh.",
    )
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    label_dir = Path(args.label_dir) if args.label_dir else None

    if not image_dir.exists():
        raise SystemExit(f"Khong tim thay thu muc anh: {image_dir}")

    if label_dir is not None and not label_dir.exists():
        raise SystemExit(f"Khong tim thay thu muc label: {label_dir}")

    pattern = "**/*" if args.recursive else "*"
    image_paths = [
        path
        for path in image_dir.glob(pattern)
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS
    ]

    bad_images = []
    for image_path in image_paths:
        bad, reason = is_bad_image(image_path, args.min_width, args.min_height)
        if bad:
            bad_images.append((image_path, reason))

    print(f"Tong so anh da quet: {len(image_paths)}")
    print(f"So anh can xoa: {len(bad_images)}")

    for image_path, reason in bad_images:
        print(f"- {image_path} ({reason})")
        if args.delete:
            image_path.unlink()
            deleted_label = delete_label_if_exists(image_path, label_dir)
            if deleted_label:
                print(f"  Da xoa label: {deleted_label}")

    if args.delete:
        print("Da xoa xong.")
    else:
        print("Moi chi xem truoc. Them --delete de xoa that.")

    if args.rename or args.rename_prefix:
        if not args.delete:
            print("Bo qua doi ten vi chua co --delete.")
            print("Them --delete neu muon xoa va doi ten that.")
            return

        rename_prefix = args.rename_prefix or image_dir.name
        renamed_paths = rename_images(image_dir, rename_prefix, label_dir, args.recursive)
        print(f"Da doi ten {len(renamed_paths)} anh con lai:")
        for renamed_path in renamed_paths:
            print(f"- {renamed_path}")


if __name__ == "__main__":
    main()
