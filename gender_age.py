import argparse
import time
import cv2 as cv


def start_detection():
    # Fonction pour obtenir la boîte englobante du visage
    def getFaceBox(net, frame, conf_threshold=0.7):
        frameHeight, frameWidth = frame.shape[:2]
        blob = cv.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1, y1, x2, y2 = int(detections[0, 0, i, 3] * frameWidth), int(
                    detections[0, 0, i, 4] * frameHeight), int(detections[0, 0, i, 5] * frameWidth), int(
                    detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
        return frame, bboxes

    faceProto, faceModel = "opencv_face_detector.pbtxt", "opencv_face_detector_uint8.pb"
    ageProto, ageModel = "age_deploy.prototxt", "age_net.caffemodel"
    genderProto, genderModel = "gender_deploy.prototxt", "gender_net.caffemodel"

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    genderList = ['Male', 'Female']

    # Charger les réseaux
    ageNet = cv.dnn.readNet(ageProto, ageModel)
    genderNet = cv.dnn.readNet(genderProto, genderModel)
    faceNet = cv.dnn.readNet(faceModel, faceProto)

    # Capturer la vidéo
    cap = cv.VideoCapture(0)
    padding = 20
    while cv.waitKey(1) < 0:
        # Lire le frame
        hasFrame, frame = cap.read()
        if not hasFrame:
            cv.waitKey()
            break
        frameFace, bboxes = getFaceBox(faceNet, frame)
        if not bboxes:
            print("Aucun visage détecté, Vérification du frame suivant")
            continue

        for bbox in bboxes:
            face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1),
                   max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
            blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]

            print("Genre : {}, confiance = {:.3f}".format(gender, genderPreds[0].max()))

            ageNet.setInput(blob)
            agePreds = ageNet.forward()
            age = ageList[agePreds[0].argmax()]

            print("Âge : {}, confiance = {:.3f}".format(age, agePreds[0].max()))

            label = "{},{}".format(gender, age)
            cv.putText(frameFace, label, (bbox[0] - 5, bbox[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2,
                       cv.LINE_AA)
            cv.imshow("Démo Genre Âge", frameFace)
            cv.imwrite(f"./detected/{int(time.time())}.jpg", frameFace)

if __name__ == "__main__":
    start_detection()