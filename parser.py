from PIL import Image
import sys
import os

def main():
    if not os.path.isdir("images"):
        print("Папка 'images' не найдена.")
        sys.exit(1)

    image_files = []
    supported_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    for filename in os.listdir("images"):
        if filename.lower().endswith(supported_ext):
            file_path = os.path.join("images", filename)
            if os.path.isfile(file_path):
                image_files.append(file_path)

    image_files.sort()

    if not image_files:
        print("В папке 'images' нет подходящих изображений.")
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
            print(f"Ошибка при обработке файла {img_path}: {e}")
            continue

    if not images:
        print("Не удалось загрузить ни одного изображения.")
        sys.exit(1)

    total_height = sum(heights)

    new_image = Image.new('RGB', (max_width, total_height), color='black')
    y_coordinates = []
    current_y = 0

    for img in images:
        y_coordinates.append(current_y)
        x_offset = (max_width - img.width) // 2
        new_image.paste(img, (x_offset, current_y))
        current_y += img.height

    new_image.save('output.jpg')

    with open('output.txt', 'w') as f:
        for y in y_coordinates:
            f.write(f"{y}\n")

if __name__ == "__main__":
    main()