from google.cloud import vision
import proto
import json
import os

def localize_objects(image_path:str) -> dict:
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api_key.json'
    client = vision.ImageAnnotatorClient()
    objects = proto.Message.to_json(client.object_localization(image=image))
    response = json.loads(objects)
    return response

def show_labels_on_image(image, response:dict) -> None:
    import cv2
    import numpy as np
    image = cv2.imread(IMAGE)
    width = image.shape[1]
    height = image.shape[0]

    for label in response['localizedObjectAnnotations']:
        label_name = label['name']
        np.random.seed(ord(label_name[0]))
        color = (np.random.randint(0,256), np.random.randint(0,256), np.random.randint(0,256))
        x1 = int(label['boundingPoly']['normalizedVertices'][0]['x'] * width)
        y1 = int(label['boundingPoly']['normalizedVertices'][0]['y'] * height)
        x2 = int(label['boundingPoly']['normalizedVertices'][2]['x'] * width)
        y2 = int(label['boundingPoly']['normalizedVertices'][2]['y'] * height)
        cv2.putText(image, label_name, (x1, y1-5), 0, 1, color, 2)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    cv2.imshow('Result', image)
    cv2.waitKey(0)

if __name__ == '__main__':
    IMAGE = ''
    response = localize_objects(IMAGE)    
    show_labels_on_image(IMAGE, response)