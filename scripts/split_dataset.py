import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", default="/home/data")
    parser.add_argument("--train_annotation", default="./data/dataset/cvmart_train.txt")
    parser.add_argument("--test_annotation", default="./data/dataset/cvmart_test.txt")

    flags = parser.parse_args()

    if os.path.exists(flags.train_annotation): os.remove(flags.train_annotation)
    if os.path.exists(flags.test_annotation): os.remove(flags.test_annotation)
    os.makedirs()
    files = os.listdir(data_path)
    xml_files = list(filter(lambda x: x.find("xml") >= 0, files))
    jpg_files = list(filter(lambda x: x.find("jpg") >= 0, files))

    pascal = pascal_voc('train', rebuild=False)