import CloudVisionAPI
import glob
import os

class BulkAnnotation:
    def __init__(self, min_score:float=0.0, custom_class_names:dict={}) -> None:
        self.min_score = min_score
        self.custom_class_names = custom_class_names
        self.class_names = {}

    @staticmethod
    def get_images_from_dir(images_dir:str='images') -> list:
        if not os.path.isdir(images_dir):
            print('images directory does not exist')
            exit()
        images = glob.glob(f'./{images_dir}/*')
        if len(images) == 0:
            print('There is no image in the folder!')
            exit()
        return images

    def parse_response(self, response:dict) -> str:
        objects = response['localizedObjectAnnotations']
        lines = []
        for object in objects:
            if self.min_score > object['score']:
                continue
            if len(self.custom_class_names): # if custom class name exists
                if object['name'] not in self.custom_class_names.keys():
                    continue
                else:
                    class_index = self.custom_class_names[object['name']]
            else:
                if object['name'] not in self.class_names.keys():
                    self.class_names[object['name']] = len(self.class_names)
                class_index = self.class_names[object['name']]
            point1 = object['boundingPoly']['normalizedVertices'][0]
            point2 = object['boundingPoly']['normalizedVertices'][2]
            x_center = (point1['x'] + point2['x']) / 2
            y_center = (point1['y'] + point2['y']) / 2
            width  = abs(point2['x'] - point1['x'])
            height = abs(point2['y'] - point1['y'])
            line = f'{class_index} {x_center} {y_center} {width} {height}'
            lines.append(line)
        return '\n'.join(lines)

    @staticmethod
    def save_as_yolo_format(content:str, image_name:str, labels_dir:str='labels') -> None:
        file_name = image_name.split('/')[-1].split('.')[0]
        os.makedirs(labels_dir, exist_ok=True)
        with open(f'{labels_dir}/{file_name}.txt', 'w') as file:
            file.write(content)

    def save_classes(self) -> None:
        if len(self.custom_class_names):
            self.class_names = self.custom_class_names
        with open('classes.txt', 'w') as file:
            file.write('\n'.join(self.class_names))

if __name__ == '__main__':
    # custom_class_names = {
    #     'Car' : 0
    # }

    bulk_annotation = BulkAnnotation()
    images = bulk_annotation.get_images_from_dir()
    for image_name in images:
        response = CloudVisionAPI.localize_objects(image_name)
        labels = bulk_annotation.parse_response(response)
        bulk_annotation.save_as_yolo_format(labels, image_name)
    bulk_annotation.save_classes()