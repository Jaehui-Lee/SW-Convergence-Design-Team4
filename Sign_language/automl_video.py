# -*- coding: utf-8 -*-
import sys
from google.cloud import automl_v1beta1 as automl
import os
import cv2
import pandas as pd
from utils import download_from_storage
import json
import csv

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"

def predict(filename, input_uri, output_uri_prefix="gs://sign_language_video_data/test_result"):
    model_id = "projects/990293478240/locations/us-central1/models/VCN3598030855617904640"

    automl_client = automl.AutoMlClient()

    # Create client for prediction service.
    # https://github.com/googleapis/python-automl/blob/0ad551a9ecdca361ff6e89d6b6d1aa74e8160eed/google/cloud/automl_v1beta1/services/prediction_service/client.py#L83
    prediction_client = automl.PredictionServiceClient()

    # Input configuration.
    input_config = dict(gcs_source={'input_uris': [input_uri]})

    # Output configration.
    output_config = dict(gcs_destination={'output_uri_prefix': output_uri_prefix})

    params = {
        "score_threshold": "0.3",
        "segment_classification": "false",
        "shot_classification": "false",
        "1s_interval_classification": "true"
    }

    # Launch long-running batch prediction operation.
    operation = prediction_client.batch_predict(
        name=model_id,
        input_config=input_config,
        output_config=output_config,
        params=params
    )

    """ dir(operation)
    ['__abstractmethods__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry', '_blocking_poll', '_cancel', '_completion_lock', '_done_callbacks', '_done_or_raise', '_exception', '_invoke_callbacks', '_metadata_type', '_operation', '_polling_thread', '_refresh', '_refresh_and_update', '_result', '_result_set', '_result_type', '_retry', '_set_result_from_operation', 'add_done_callback', 'cancel', 'cancelled', 'deserialize', 'done', 'exception', 'metadata', 'operation', 'result', 'running', 'set_exception', 'set_result']
    """
    print("Waiting result...")
    operation.result()

    print('Batch predict operation started: ', operation.metadata)
    
    gs_json = operation.metadata.batch_predict_details.output_info.gcs_output_directory

    # gs_json = gs_json_dir + "/" + filename + "_1.json"
    download_from_storage(gs_json + "/" + filename + "_1.json")
    
    return 'downloads/' + filename + '_1.json'

def make_csv(file_path):

    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    gs_path = 'gs://sign_language_video_data/JW_test/' + file_path.split('/')[-1]
    filename = file_path.split('/')[-1]
    start = 0
    end = str(round(duration, 2))

#    csv = {'gs_path':[gs_path], 'start':[start], 'end':[end]}
#    # print(csv)
#    df = pd.DataFrame(csv)
#    df.to_csv('static/uploads/sign_language_video_test_' + filename + '.csv', header=False, index=False, encoding='utf-8')
    data = [[gs_path, str(start), str(end)]]
    f = open('static/uploads/sign_language_video_test_' + filename + '.csv', "w")
    writer = csv.writer(f)

    writer.writerows(data)
    f.close()
    
    return 'sign_language_video_test_' + filename + '.csv'


def _download_json(path, filename):
    gs_json = path + "/" + filename + "_1.json"
    print(gs_json)
    download_from_storage(gs_json)

    return 'downloads/' + filename + '_1.json'

def parsing_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f)

    word_list = []

    # find confidence 1s_interval_classification
    confidence = 0
    for entry in json_data["one_second_interval_classification_annotations"]:
        for i in range(len(entry["frames"])):
            if entry["frames"][i]["confidence"] >= 0.3:
                display_name = entry["annotation_spec"]["display_name"]
                confidence = entry["frames"][i]["confidence"]
                seconds = entry["frames"][i]["time_offset"]["seconds"]
                nanos = entry["frames"][i]["time_offset"]["nanos"]
                # list의 마지막 element가 똑같은 단어가 아니면 추가
                if len(word_list) == 0 or word_list[-1][0] != display_name:
                    word_list.append([display_name, confidence, seconds, nanos])
                # list의 마지막 element가 똑같은 단어면 confidence를 비교해서 크면 삭제 후 추가
                elif word_list[-1][0] == display_name and word_list[-1][1] < confidence:
                    del (word_list[-1])
                    word_list.append([display_name, confidence, seconds, nanos])

    # sort by <seconds>
    word_list.sort(key=lambda word: word[2])
    # print(word_list)

    # add words to sentence
    sentence = ""
    for i in range(len(word_list)):
        sentence += word_list[i][0]
        if i != len(word_list) - 1:
            sentence += " "

    return sentence


if __name__ == "__main__":
    predict('gs://sign_language_video_data/JW_test/sign_language_video_test_3.__.mp4.csv')
