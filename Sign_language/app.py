from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import sys

sys.path.append('/')
import automl_video, automl_nlp
from utils import upload_to_storage, download_from_storage, get_raw_filename

def create_app():
    app = Flask(__name__)

# --------------------------------- [edit] ---------------------------------- #
    @app.route('/')
    def render_file():
        return render_template("index.html")

    @app.route('/fileupload', methods=['POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['videofile']

            file_path = 'static/uploads/' + secure_filename(f.filename)
            f.save(file_path)

            # upload video file to google cloud storage
            upload_to_storage(file_path)

            # make csv for video prediction
            csv = automl_video.make_csv(file_path)

            # upload csv to google cloud storage
            upload_to_storage('static/uploads/' + csv)

            # predict automl video intelligence
            json_path = automl_video.predict(filename=get_raw_filename(file_path), input_uri='gs://sign_language_video_data/JW_test/'+csv)
            print(json_path)
            # download test json to server
            words = automl_video.parsing_json(json_path)

            # nlp predict
            sentence, accurancy = automl_nlp.predict(words)

            result = "<" + sentence + "> accurancy : " + str(accurancy)

            return render_template('fileupload.html', result=result, data="uploads/" + f.filename)
            
# --------------------------------------------------------------------------- #

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
