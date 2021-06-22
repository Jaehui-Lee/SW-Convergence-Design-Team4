# -*- coding: utf-8 -*-
from google.cloud import automl_v1beta1 as automl
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "key.json"

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

# TODO(developer): Uncomment and set the following variables
project_id = "automl-video-test-292702"
model_id = "TCN6194989359494594560"

def predict(content):

    prediction_client = automl.PredictionServiceClient()

    # Get the full path of the model.
    model_full_id = automl.AutoMlClient.model_path(project_id, "us-central1", model_id)

    # Supported mime_types: 'text/plain', 'text/html'
    # https://cloud.google.com/automl/docs/reference/rpc/google.cloud.automl.v1#textsnippet
    text_snippet = automl.TextSnippet(content=content, mime_type="text/plain")
    payload = automl.ExamplePayload(text_snippet=text_snippet)

    response = prediction_client.predict(name=model_full_id, payload=payload)

    """ for annotation_payload in response.payload:
        print(u"Predicted class name: {}".format(annotation_payload.display_name))
        print(
            u"Predicted class score: {}".format(annotation_payload.classification.score)
        ) """

    #print(u"Predicted class name: {}".format(response.payload[0].display_name))
    return trans_label[response.payload[0].display_name], response.payload[0].classification.score

if __name__ == "__main__":
    content = "코로나 가다 검사"
    sentence, accurancy = predict(content)
    print(sentence)
