import os
import glob
# 필요한 패키지 import
import imutils  # 파이썬 OpenCV가 제공하는 기능 중 복잡하고 사용성이 떨어지는 부분을 보완(이미지 또는 비디오 스트림 파일 처리 등)
import cv2  # opencv 모듈

path_dir = '/Users/jwon/Desktop/sign'
file_list = os.listdir(path_dir)

file_list.sort()
print(file_list)

# for dir in file_list:
#
#     if dir == '.DS_Store':
#         continue
#
#     path = path_dir + '/' + dir + '/*'
#     us_path = [p for p in glob.glob(path)]
#
#     for video in us_path:
#         print(video)
#         print("[video 시작]")
#         vs = cv2.VideoCapture(video)
#
#         result_path = video.replace('sign', 'NewData').replace('MOV', 'avi')
#         print(result_path)
#         # result_path = "/Users/jwon/Desktop/result_video.avi"
#         # print(result_path)
#
#         writer = None
#
#         # 비디오 스트림 프레임 반복
#         while True:
#             # 프레임 읽기
#             ret, frame = vs.read()
#
#             # 읽은 프레임이 없는 경우 종료
#             if frame is None:
#                 break
#
#             # 프레임 resize
#             frame = imutils.resize(frame, width=300)
#
#             # # 프레임 출력
#             # cv2.imshow("frame", frame)
#             #
#             # # 'q' 키를 입력하면 종료
#             # key = cv2.waitKey(1) & 0xFF
#             # if key == ord("q"):
#             #     break
#
#             # 저장할 비디오 설정
#             if writer is None:
#                 fourcc = cv2.VideoWriter_fourcc(*"MJPG")
#                 writer = cv2.VideoWriter(result_path, fourcc, 25, (frame.shape[1], frame.shape[0]), True)
#
#             # 비디오 저장
#             if writer is not None:
#                 writer.write(frame)
#
#         # 종료
#         vs.release()
#         cv2.destroyAllWindows()
#
