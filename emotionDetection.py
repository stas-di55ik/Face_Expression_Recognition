import cv2
from fer import FER
import os

import markers

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
emotion_detector = FER(mtcnn=True)


class RecognizedPhoto:
    def __init__(self, fn, sum, success):
        self.file_name = fn
        self.summary = sum
        self.succeeded = success


def find_crop_faces(file_id):
    # Had better if there would be some try block or handling timer
    input_image = cv2.imread(file_id)
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(
        gray_image,
        scaleFactor=1.25,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    output_images = []

    for (x, y, w, h) in faces:
        x1 = int(x - 0.13 * w)
        y1 = int(y - 0.13 * h)
        x2 = int(x + 1.13 * w)
        y2 = int(y + 1.13 * h)
        current_face = input_image[y1:y2, x1:x2]
        output_filename = str(x+y) + file_id
        output_images.append(output_filename)
        cv2.imwrite(output_filename, current_face)

    return output_images


def detect_emotions(file_id):
    all_input_images = find_crop_faces(file_id)
    recognized_photos = []
    for img in all_input_images:
        summary = ''
        input_image = cv2.imread(img)
        try:
            result = emotion_detector.detect_emotions(input_image)

            bounding_box = result[0]["box"]
            emotions = result[0]["emotions"]
            cv2.rectangle(input_image, (bounding_box[0], bounding_box[1]), (
                bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                        (0, 155, 255), 2,)

            emotion_name, score = emotion_detector.top_emotion(input_image)
            for index, (emotion_name, score) in enumerate(emotions.items()):
                color = (211, 211, 211) if score < 0.01 else (255, 0, 0)
                emotion_score = "{}: {}".format(emotion_name, "{:.2f}".format(score))
                summary += emotion_score + '\n'

                # This is score text on the photo
                # cv2.putText(input_image, emotion_score,
                #             (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + index * 15),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA, )
            succeeded = True
        except:
            succeeded = False
        new_filename = markers.Detected_emotions_tag + img
        cv2.imwrite(new_filename, input_image)
        recognized_photo = RecognizedPhoto(new_filename, summary, succeeded)
        recognized_photos.append(recognized_photo)
        os.remove(img)

    return recognized_photos

