import os
import argparse
import xml.etree.ElementTree as ET
import re


def convert_voc_annotation(data_path, data_type, anno_path, use_difficult_bbox=True):

    classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
               'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
               'motorbike', 'person', 'pottedplant', 'sheep', 'sofa',
               'train', 'tvmonitor']
    img_inds_file = os.path.join(
        data_path, 'ImageSets', 'Main', data_type + '.txt')
    with open(img_inds_file, 'r') as f:
        txt = f.readlines()
        image_inds = [line.strip() for line in txt]

    with open(anno_path, 'a') as f:
        for image_ind in image_inds:
            image_path = os.path.join(
                data_path, 'JPEGImages', image_ind + '.jpg')
            annotation = image_path
            label_path = os.path.join(
                data_path, 'Annotations', image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            for obj in objects:
                difficult = obj.find('difficult').text.strip()
                if (not use_difficult_bbox) and(int(difficult) == 1):
                    continue
                bbox = obj.find('bndbox')
                class_ind = classes.index(
                    obj.find('name').text.lower().strip())
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()
                annotation += ' ' + \
                    ','.join([xmin, ymin, xmax, ymax, str(class_ind)])
            print(annotation)
            f.write(annotation + "\n")
    return len(image_inds)


def parse_annotation(data_path, filename_list, anno_path, use_difficult_bbox=True):

    classes = ['vendors']
    files = os.listdir(data_path)
    xml_files = list(filter(lambda x: x.find("xml") >= 0, files))
    file_inds_list = map(lambda x: re.sub('[\.xml]', '', x), xml_files)

    with open(anno_path, 'a') as f:
        for image_ind in file_inds_list:
            image_path = os.path.join(
                data_path, image_ind + '.jpg')
            annotation = image_path
            label_path = os.path.join(
                data_path, image_ind + '.xml')
            root = ET.parse(label_path).getroot()
            objects = root.findall('object')
            for obj in objects:
                bbox = obj.find('bndbox')
                class_ind = classes.index(
                    obj.find('name').text.lower().strip())
                xmin = bbox.find('xmin').text.strip()
                xmax = bbox.find('xmax').text.strip()
                ymin = bbox.find('ymin').text.strip()
                ymax = bbox.find('ymax').text.strip()
                annotation += ' ' + \
                              ','.join([xmin, ymin, xmax, ymax, str(class_ind)])
            print(annotation)
            f.write(annotation + "\n")
    return len(file_inds_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/home/data/51")
    parser.add_argument("--train_annotation",
                        default="./data/dataset/cvmart_train.txt")
    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation):
        os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation):
        os.remove(flags.test_annotation)

    num1 = convert_voc_annotation(os.path.join(
        flags.data_path, 'train/VOCdevkit/VOC2007'), 'trainval', flags.train_annotation, False)
    print('=> The number of image for train is: %d' % num1)
