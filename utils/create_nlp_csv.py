# -*- coding: utf-8 -*-

#make .csv of learning data

import os
import glob
import pandas as pd
import cv2

#label = ['hi', 'what', 'meat', 'bi bim rice', 'glad', 'hobby', 'me', 'movie', 'face', 'see', 'name', 'read', 'thank', 'equal', 'sorry', 'eat', 'fine', 'do effort', 'next', 'age', 'again', 'how many', 'day', 'good, nice', 'when', 'we', 'subway', 'friendly', 'bus', 'ride', 'cell phone', 'where', 'number', 'location', 'guide', 'responsibility', 'who', 'arrive', 'family', 'time', 'introduction', 'receive', 'please?', 'walk', 'parents', '10 minutes', 'sister', 'study', 'human', 'now', 'special', 'yesterday', 'education', 'test', 'end', 'you', 'worried about', 'marry', 'effort', 'no', 'sweat', 'yet', 'finally', 'born', 'success', 'favor', 'Seoul', 'dinner', 'experience', 'invite', 'food', 'want', 'visit', 'one hour', 'far', 'good', 'care']
#label = ['오한', '가래', '확진자', '발열', '가슴', '불면', '기침', '콧물', '목', '팔', '다리', '어깨', '무릎', '손', '발', '허리', '입원', '알레르기', '코로나', '검사', '약국', '안내소', '진료소', '건강검진', '병원', '수화', '통역사', '약', '어디', '접촉', '방법', '다시', '감기', '몸살', '두통', '배탈', '오다', '먹다', '있다', '아프다', '나오다', '생기다', '답답하다', '받다', '걸리다', '다치다', '현기증', '감사합니다', '뜨겁다']
class_label = ['코로나 검사 받으러 왔습니다.','코로나 확진자와 접촉했습니다.', '안내소 어디에 있나요?', '약국 어디인가요?', "두통과 열이 있습니다."]

path_dir = '/Users/jwon/Desktop/nlp/'
file_list = os.listdir(path_dir)

file_list.sort()
print(file_list)

csvdict = {'usage':[],'file_path':[],'class_label':[]}

count = 0
for dir in file_list:

    if dir == '.DS_Store':
        continue

    path = path_dir + '/' + dir + '/*'
    us_path = [p for p in glob.glob(path)]

    for file_path in us_path:

        filename = file_path.split('/')[-1]
        usage = "TRAIN"
        file_path = 'gs://sign_language_nlp_data/nlp/'+dir+'/'+filename
        class_label = dir

        csvdict['usage'].append(usage)
        csvdict['file_path'].append(file_path)
        print(filename)
        csvdict['class_label'].append(class_label)
        count += 1

    print(path_dir, count)

print(set(csvdict['class_label']))
# df = pd.DataFrame(csvdict)
# print(df)
# df.to_csv(path_dir+'sign_language_video.csv', index=False, encoding='utf-8')