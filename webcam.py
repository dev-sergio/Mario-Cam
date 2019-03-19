import cv2
import pyautogui


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    altura, largura = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(150, 150),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

        if x > 250:

            print("Ir pra esquerda")
        if x < 200:
            print("Ir pra direita")
        if y < 100:
            print("Pular")

    # Display the resulting frame

    #novo ===========
    ponto = (0, 0)
    rotacao = cv2.getRotationMatrix2D(ponto, 0, 0.5)
    rotacionado = cv2.warpAffine(frame, rotacao, (largura, altura))
    cv2.imshow('Video', rotacionado)
    cv2.resizeWindow('Video', 320, 240)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
