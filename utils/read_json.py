#bring confidence from <result.json> file
#write .txt .csv file

import json
import csv

with open('Address/filename', 'r') as f :
    json_data = json.load(f)

#print file name
print(f.name.split("/")[-1])

word_list = []

#find confidence 1s_interval_classification
confidence = 0
for entry in json_data["one_second_interval_classification_annotations"] :
    for i in range(len(entry["frames"])):
        if entry["frames"][i]["confidence"] >= 0.3 :
            display_name = entry["annotation_spec"]["display_name"]
            confidence = entry["frames"][i]["confidence"]
            seconds = entry["frames"][i]["time_offset"]["seconds"]
            nanos = entry["frames"][i]["time_offset"]["nanos"]
            #list의 마지막 element가 똑같은 단어가 아니면 추가
            if len(word_list) == 0 or word_list[-1][0] != display_name :
                word_list.append([display_name, confidence, seconds, nanos])
            #list의 마지막 element가 똑같은 단어면 confidence를 비교해서 크면 삭제 후 추가
            elif word_list[-1][0] == display_name and word_list[-1][1] < confidence :
                del(word_list[-1])
                word_list.append([display_name, confidence, seconds, nanos])
            

#find confidence segment_classification
''' for entry in json_data["segment_classification_annotations"] :
    for i in range(len(entry["segments"])):
        if entry["segments"][i]["confidence"] >= 0.3 :
            display_name = entry["annotation_spec"]["display_name"]
            confidence = entry["segments"][i]["confidence"]
            start = entry["segments"][i]["segment"]["start_time_offset"]["seconds"]
            end = entry["segments"][i]["segment"]["end_time_offset"]["seconds"]
            #list의 마지막 element가 똑같은 단어가 아니면 추가
            if len(word_list) == 0 or word_list[-1][0] != display_name :
                word_list.append([display_name, confidence, start, end])
            #list의 마지막 element가 똑같은 단어면 confidence를 비교해서 크면 삭제 후 추가
            elif word_list[-1][0] == display_name and word_list[-1][1] < confidence :
                del(word_list[-1])
                word_list.append([display_name, confidence, start, end]) '''


#sort by <seconds>
word_list.sort(key=lambda word: word[2])
print(word_list)

#add words to sentence
sentence = ""
for i in range(len(word_list)):
    sentence += word_list[i][0]
    if i != len(word_list)-1 :
        sentence += " "

#json file close
f.close()

''' #write .txt
f = open("1.txt", 'w')

for i, element in zip(range(len(word_list)), word_list):
    f.write(element[0])
    if i != len(word_list)-1 :
        f.write(' ')
        
#txt file close
f.close()

with open('1.csv','w') as f :
    wr=csv.writer(f)
    wr.writerow(["gs://sign_language_nlp_data/1.txt"]) '''