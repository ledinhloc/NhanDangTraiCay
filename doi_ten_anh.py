import os

folder_path = r"Image\Chuoi"
class_name = "Chuoi"

image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')

files = [
    f for f in os.listdir(folder_path)
    if f.lower().endswith(image_extensions)
]

files.sort()

# Bước 1: đổi sang tên tạm
temp_files = []

for i, old_name in enumerate(files):
    old_path = os.path.join(folder_path, old_name)

    temp_name = f"__temp__{i}.tmp"
    temp_path = os.path.join(folder_path, temp_name)

    os.rename(old_path, temp_path)

    temp_files.append(temp_name)

# Bước 2: đổi sang tên cuối cùng
for index, temp_name in enumerate(temp_files, start=1):
    temp_path = os.path.join(folder_path, temp_name)

    new_name = f"{class_name}_{index}.jpg"
    new_path = os.path.join(folder_path, new_name)

    os.rename(temp_path, new_path)

    print(f"{temp_name} -> {new_name}")

print("Hoàn thành!")