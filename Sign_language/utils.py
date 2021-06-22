import os

def upload_to_storage(file_path, destination='gs://sign_language_video_data/JW_test'):
    os.system('gsutil cp ' + file_path + ' ' + destination)

def download_from_storage(file_path, destination='downloads'):
    os.system('gsutil cp ' + file_path + ' ' + destination)

# get only file name
def get_raw_filename(filename):
    rawname = os.path.splitext(filename)[0]
    rawname = rawname.split('/')[-1]

    return rawname
