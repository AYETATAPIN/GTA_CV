import uuid

from PIL import Image
import sys
import os

def license_plate_pars(license_dir):
    if not os.path.isdir(license_dir):
        return "badDirectory", []

    image_files = []
    supported_ext = ('.jpg', '.jpeg')

    for filename in os.listdir(license_dir):
        if filename.lower().endswith(supported_ext):
            file_path = os.path.join(license_dir, filename)
            if os.path.isfile(file_path):
                image_files.append(file_path)

    if not image_files:
        print(f"В директории {license_dir} нет подходящих изображений.")
        sys.exit(1)

    images = []
    heights = []
    max_width = 0

    for img_path in image_files:
        try:
            img = Image.open(img_path).convert('RGB')
            images.append(img)
            width, height = img.size
            heights.append(height)
            if width > max_width:
                max_width = width
        except Exception as e:
            return f"BadImage {img_path} with {e}", []

    if not images:
        return "BadImages", []

    total_height = sum(heights)

    new_image = Image.new('RGB', (max_width, total_height), color='black')
    y_coordinates = []
    current_y = 0

    for img in images:
        y_coordinates.append(current_y)
        x_offset = (max_width - img.width) // 2
        new_image.paste(img, (x_offset, current_y))
        current_y += img.height

    str_name = str(uuid.uuid4())
    new_image.save(str_name + '.jpg')
    return str_name, y_coordinates

if __name__ == "__main__":
    print(license_plate_pars("images"))