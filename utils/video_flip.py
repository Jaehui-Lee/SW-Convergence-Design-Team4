import numpy as np
import cv2

video = "/Users/jwon/Desktop/video.avi"
vs = cv2.VideoCapture(video)
result_path = "/Users/jwon/Desktop/result_video.avi"

# 비디오 저장 변수
writer = None

# 비디오 스트림 프레임 반복
while True:
    # 프레임 읽기
    ret, frame = vs.read()

    if frame is None:
        break

    frame = cv2.flip(frame, 1)

    # 저장할 비디오 설정
    if writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(result_path, fourcc, 25, (frame.shape[1], frame.shape[0]), True)

    # 비디오 저장
    if writer is not None:
        writer.write(frame)

# 종료
vs.release()
cv2.destroyAllWindows()