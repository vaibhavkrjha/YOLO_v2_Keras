from PIL import Image
import imageio
from keras import backend as K
from keras.models import load_model
import cv2
import numpy as np
import os
from os.path import isfile, join

from yolo_utils import read_classes, read_anchors, generate_colors, preprocess_image, draw_boxes

from yad2k.models.keras_yolo import yolo_head, yolo_eval

import cv2

vidcap = cv2.VideoCapture('/Users/prachis/pet_projects/YOLOv2_keras/video.mp4')
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        path = "/Users/prachis/pet_projects/YOLOv2_keras/images/"
        cv2.imwrite(os.path.join(path, "image"+str(count)+".jpg"), image)
        # cv2.imwrite("image"+str(count)+".jpg", image)     # save frame as JPG file

        input_image_name = "image"+str(count)+".jpg"

        # Obtaining the dimensions of the input image
        input_image = Image.open(
            "/Users/prachis/pet_projects/YOLOv2_keras/images/" + input_image_name)
        width, height = input_image.size
        width = np.array(width, dtype=float)
        height = np.array(height, dtype=float)

        # Assign the shape of the input image to image_shapr variable
        image_shape = (height, width)

        # Loading the classes and the anchor boxes that are provided in the madel_data folder
        class_names = read_classes("model_data/coco_classes.txt")
        anchors = read_anchors("model_data/yolo_anchors.txt")

        # Load the pretrained model. Please refer the README file to get info on how to obtain the yolo.h5 file
        yolo_model = load_model("model_data/yolo.h5")

        # Print the summery of the model
        # yolo_model.summary()

        # Convert final layer features to bounding box parameters
        yolo_outputs = yolo_head(yolo_model.output, anchors, len(class_names))

        # Now yolo_eval function selects the best boxes using filtering and non-max suppression techniques.
        # If you want to dive in more to see how this works, refer keras_yolo.py file in yad2k/models
        boxes, scores, classes = yolo_eval(yolo_outputs, image_shape)

        # Initiate a session
        sess = K.get_session()

        # Preprocess the input image before feeding into the convolutional network
        image, image_data = preprocess_image("/Users/prachis/pet_projects/YOLOv2_keras/images/" +
                                             input_image_name, model_image_size=(608, 608))

        # Run the session
        out_scores, out_boxes, out_classes = sess.run([scores, boxes, classes],
                                                      feed_dict={yolo_model.input: image_data,
                                                                 K.learning_phase(): 0})

        # Print the results
        print('Found {} boxes for {}'.format(len(out_boxes), input_image_name))
        # Produce the colors for the bounding boxs
        colors = generate_colors(class_names)
        # Draw the bounding boxes
        draw_boxes(image, out_scores, out_boxes, out_classes, class_names, colors)
        # Apply the predicted bounding boxes to the image and save it
        image.save(os.path.join("/Users/prachis/pet_projects/YOLOv2_keras/out/",
                                input_image_name), quality=90)
        output_image = imageio.imread(os.path.join(
            "/Users/prachis/pet_projects/YOLOv2_keras/out/", input_image_name))

    return hasFrames
sec = 0
frameRate = 0.5 #//it will capture image in each 0.5 second
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)


pathIn = '/Users/prachis/pet_projects/YOLOv2_keras/out/'
pathOut = '/Users/prachis/pet_projects/YOLOv2_keras/video.avi'
fps = 0.5
frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
# for sorting the file names properly
files.sort(key=lambda x: x[5:-4])
files.sort()
frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
# for sorting the file names properly
files.sort(key=lambda x: x[5:-4])
for i in range(len(files)):
    filename = pathIn + files[i]
    # reading each files
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)

    # inserting the frames into an image array
    frame_array.append(img)
out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
out.release()





