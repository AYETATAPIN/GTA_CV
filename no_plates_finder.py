import cv2 as cv
import os

#Находит в указанных папках датасета всю разметку, где нет ни одного номерного знака

#Вывод изображения с отрисовкой ББ
def view_image(filename, lines):
    image_path = os.path.join(images_path, filename[:-3] + "jpg")
    im = cv.imread(image_path)
    for line in [arr.split() for arr in lines]:
        start_point = (int(im.shape[1] * (float(line[1]) - float(line[3])/2)), int(im.shape[0] * (float(line[2]) - float(line[4])/2)))
        end_point = (int(im.shape[1] * (float(line[1]) + float(line[3])/2)), int(im.shape[0] * (float(line[2]) + float(line[4])/2)))
        cv.rectangle(im, start_point, end_point, (255, 0, 0))
    cv.imshow(filename, im)
    cv.waitKey(0)
    cv.destroyAllWindows()

#Нужно указать путь до папок соответственно с разметкой и изображениями
labels_path = 'datasets/cvat/labels/val'
images_path = 'datasets/cvat/images/val'
show_images = True #Можно отключить показ изображений, тогда просто запишется в фаил список подходящих файлов разметки
with open("no_plates_result.txt", "w") as result:

    for filename in os.listdir(labels_path):
        file_path = os.path.join(labels_path, filename)
        if os.path.isfile(file_path):
            b = True
            with open(file_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if(line[0] == '1'):
                        b = False
                        break
                if(b):
                    result.write(file_path + "\n")
                    if(show_images):
                        view_image(filename, lines)

