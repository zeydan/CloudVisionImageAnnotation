import cv2
import numpy as np

def get_labels_from_file(label_file:str) -> list:
    with open(label_file, 'r') as file:
        lines = file.read()
    if len(lines) == 0:
        print('There is no label for this image.')
        exit()
    labels = []
    for line in lines.split('\n'):
        columns = line.split(' ')
        label = {
            'label_no': int(columns[0]),
            'x_center': float(columns[1]),
            'y_center': float(columns[2]),
            'width'   : float(columns[3]),
            'height'  : float(columns[4])
        }
        labels.append(label)
    return labels

def get_class_names_from_file(classes_file:str) -> dict:
    with open(classes_file, 'r') as file:
        lines = file.read()
    classes = {}
    for i, line in enumerate(lines.split('\n')):
        classes[i] = line
    return classes

def draw_bounding_box(image, labels, classes:dict={}) -> None:
    width = image.shape[1]
    height = image.shape[0]

    for label in labels:
        np.random.seed(label['label_no'])
        color = (np.random.randint(0,256), np.random.randint(0,256), np.random.randint(0,256))
        label_name = str(label['label_no'])
        if len(classes) > 0:
            label_name = classes[label['label_no']]
        x1 = int((label['x_center'] - (label['width'] / 2)) * width)
        y1 = int((label['y_center'] - (label['height'] / 2)) * height)
        x2 = int((label['x_center'] + (label['width'] / 2)) * width)
        y2 = int((label['y_center'] + (label['height'] / 2)) * height)
        cv2.putText(image, label_name, (x1, y1-5), 0, 1, color, 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

if __name__ == '__main__':
    IMAGE = ''
    LABEL = ''
    CLASSES = 'classes.txt'

    image = cv2.imread(IMAGE)
    labels = get_labels_from_file(LABEL)
    classes = get_class_names_from_file(CLASSES)

    draw_bounding_box(image, labels, classes)

    cv2.imshow('Result', image)
    cv2.waitKey(0)