import itertools
import pandas as pd
import nlp_data
import glob
import os

path_dir = '/Users/jwon/Desktop/'

word_label = ['코로나 검사 받으러 왔습니다.', "코로나 검사 어디서 받나요?", '코로나 검사는 어떻게 하나요?',
              '코로나 확진자와 접촉했습니다.', "언제 다시 병원에 오면 되나요?", '수화 통역사 있나요?',
              '선별진료소가 어디인가요?', '목이 아픕니다.', '두통이 있습니다.',
              '약을 어디서 받나요?', '알레르기가 있다.', '기침이 나옵니다.',
              '콧물이 나옵니다', '기침과 콧물이 나온다', '불면증이 있습니다.',
              '팔이 아픕니다.', '다리를 다쳤습니다', '배탈이 나다.',
              '몸살이 나다', '가래가 나오다', '현기증이 있다',
              '입원하러 오다', '감기에 걸리다', '열이 있습니다',
              '허리를 다쳤습니다', '손을 다쳤습니다', '발을 다쳤습니다.',
              '어깨가 아픕니다', '가슴이 답답합니다', '두통과 열이 있다',
              '가슴이 아프다', '약 복용 방법은 어떻게 되나요?', '약국이 어디에 있나요?',
              '안내소 어디에 있나요?']

class_label = ['corona test come', 'corona test where', 'corona test how',
               'contact cofirmed',  'when back hospital', 'have interpreter',
               'clinic where', 'sore throat', 'headache',
               'where to get medicine', 'have allergy', 'Cough',
               'runny nose', 'cough and runny nose', 'Insomnia',
               'arm hurts', 'leg hurts', 'upset stomach',
               'body aches', 'Garae', 'Dizziness',
               'Hospitalize', 'have cold', 'Fever',
               'waist hurts', 'hands hurts', 'foot hurts',
               'shoulder hurts', 'stuffy chest', 'headache fever',
               'chest hurts', 'how to take medicine', 'pharmacy where',
               'information where']

trans_label = dict(zip(class_label, word_label))
# print(trans_label)

words = {}
words = nlp_data.data_upload()

usage = []
sentence = []
c_label = []

total_count = 0
for label, word_list in words.items():
    word_count = 0
    for word in word_list:
        permut = list(map(' '.join, itertools.permutations(word)))
        print(permut)
        count = len(permut)

        if word_list[-1] is word:
            usage = usage + ["VALIDATION"] * count
            usage[-1] = "TEST"
        else:
            usage = usage + ["TRAIN"] * count
        sentence = sentence + permut
        c_label = c_label + [label] * count

        word_count += count

    total_count += word_count
    print(word_count)
print(total_count)

csvdict = {'usage':usage,'sentence':sentence,'class_label':c_label}
df = pd.DataFrame(csvdict)
print(df)
df.to_csv(path_dir+'sign_language_nlp.csv', index=False, encoding='utf-8')

