import uuid

from PIL import Image
import os

def combine_plates(license_plates_dir):
    if not os.path.isdir(license_plates_dir):
        return "BadDirectory", []

    image_names = []
    supported_ext = ('.jpg', '.jpeg')

    for filename in os.listdir(license_plates_dir):
        if filename.lower().endswith(supported_ext):
            file_path = os.path.join(license_plates_dir, filename)
            if os.path.isfile(file_path):
                image_names.append(file_path)

    if not image_names:
        return f"В директории {license_plates_dir} нет подходящих изображений.", []

    image_files = []
    heights = []
    max_width = 0

    plate_names_and_y_coords = []

    for img_path in image_names:
        try:
            img = Image.open(img_path).convert('RGB')
            image_files.append(img)
            width, height = img.size
            heights.append(height)
            plate_names_and_y_coords.append([img_path])
            if width > max_width:
                max_width = width
        except Exception as e:
            return f"BadImage {img_path} with {e}", []

    if not image_files:
        return "BadImages", []

    total_height = sum(heights)

    new_image = Image.new('RGB', (max_width, total_height), color='black')
    current_y = 0
    index = 0

    for img in image_files:
        plate_names_and_y_coords[index].append(current_y)
        index += 1
        x_offset = (max_width - img.width) // 2
        new_image.paste(img, (x_offset, current_y))
        current_y += img.height

    os_random_int = str(uuid.uuid4())
    str_name = f"{license_plates_dir}/{os_random_int}.jpg"
    new_image.save(str_name)
    return str_name, plate_names_and_y_coords

# if __name__ == "__main__":
#     print(combine_plates(
#         "D:/prg/zalupen/crops/mystream__2025_05_05_19_13_47__a4f3b2ba-2290-46b0-8811-bba732120cbe/License plate"))
