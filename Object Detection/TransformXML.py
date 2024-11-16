import os
import shutil
import random
import xml.etree.ElementTree as ET

inputDir = './Datasets/For YOLO/ML-Data'
trainImgDir = './Datasets/For YOLO/Bee/images/train'
valImgDir = './Datasets/For YOLO/Bee/images/val'
trainLabelDir = './Datasets/For YOLO/Bee/labels/train'
valLabelDir = './Datasets/For YOLO/Bee/labels/val'

os.makedirs(trainImgDir, exist_ok=True)
os.makedirs(valImgDir, exist_ok=True)
os.makedirs(trainLabelDir, exist_ok=True)
os.makedirs(valLabelDir, exist_ok=True)

def convertToYolo(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

xmlFiles = [f for f in os.listdir(inputDir) if f.endswith(".xml")]
random.shuffle(xmlFiles)
splitIndex = int(len(xmlFiles) * 0.8)
trainFiles = xmlFiles[:splitIndex]
valFiles = xmlFiles[splitIndex:]

for dataset, files, imgDir, labelDir in [('train', trainFiles, trainImgDir, trainLabelDir),
                                           ('val', valFiles, valImgDir, valLabelDir)]:
    for filename in files:
        xmlFile = os.path.join(inputDir, filename)
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        outputFile = os.path.join(labelDir, filename.replace(".xml", ".txt"))
        with open(outputFile, 'w') as yoloFile:
            for obj in root.findall('object'):
                label = obj.find('name').text
                if label != 'bee':
                    continue
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)
                yoloBox = convertToYolo((width, height), (xmin, xmax, ymin, ymax))
                yoloFile.write(f"0 {yoloBox[0]} {yoloBox[1]} {yoloBox[2]} {yoloBox[3]}\n")
        
        for ext in ['.jpg', '.jpeg', '.png']:
            imageName = filename.replace(".xml", ext)
            imagePath = os.path.join(inputDir, imageName)
            if os.path.exists(imagePath):
                destination = os.path.join(imgDir, imageName)
                shutil.copy(imagePath, destination)
                break
        else:
            print(f"Image corresponding to {filename} not found, skipping...")

print("Dataset split completed.")
