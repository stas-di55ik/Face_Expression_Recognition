import cv2
from fer import FER
import os

import markers


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
emotion_detector = FER(mtcnn=True)


def emotion_detection(file_id, file_extension):
    try:
        summary = ''
        input_image = cv2.imread(file_id + file_extension)
        result = emotion_detector.detect_emotions(input_image)

        bounding_box = result[0]["box"]
        emotions = result[0]["emotions"]
        cv2.rectangle(input_image, (
        bounding_box[0], bounding_box[1]), (
            bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                      (0, 155, 255), 2,)

        emotion_name, score = emotion_detector.top_emotion(input_image)
        for index, (emotion_name, score) in enumerate(emotions.items()):
            color = (211, 211, 211) if score < 0.01 else (255, 0, 0)
            emotion_score = "{}: {}".format(emotion_name, "{:.2f}".format(score))
            summary += emotion_score + '\n'
            cv2.putText(input_image, emotion_score,
                        (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + index * 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA, )

        cv2.imwrite(markers.Detected_emotions_tag + file_id + file_extension, input_image)
        return summary

    except:
        return markers.Error
