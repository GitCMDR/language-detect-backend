from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort

from langdetect import DetectorFactory, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from iso639 import languages

app = Flask(__name__)
api = Api(app)

# Language Detector is non-deterministic. Enforce consistent results by defining a seed value.
SEED = 10
DetectorFactory.seed = SEED

parser = reqparse.RequestParser()
parser.add_argument('text', required=True, help='Text field is required.')


@app.route('/loaderio-a671a78cb4c0fc9aeb348ff183ce7147/')
def loader_io():
    return "loaderio-a671a78cb4c0fc9aeb348ff183ce7147"


class LanguageDetect(Resource):
    def post(self):
        # Verify input
        args = parser.parse_args()

        # Retrieve text input from POST request
        input_text = args['text']

        try:
            # Detect language of text and store resulting list in 'result'
            result = detect_langs(input_text)

            # Grab the first/top language code (highest confidence)
            language = result[0]

            # Retrieve the name of the language by mapping resulting language code (in ISO 639-1)
            # to its language name - https://en.wikipedia.org/wiki/ISO_639-1
            language_name = languages.get(alpha2=language.lang).name

            # Grab the first/top language result confidence and round up to two decimals.
            language_confidence = round(language.prob, 2)

            return jsonify({
                "text": input_text,
                "language": language_name,
                "confidence": language_confidence
            })

        except LangDetectException:
            abort(400, text="Bad Request - Text must not have numeric or special characters only and must "
                            "contain at least 1 letter.")


# noinspection PyTypeChecker
# https://github.com/flask-restful/flask-restful/commit/f815437784273e5e16f43d1253d59e585cf411f6
api.add_resource(LanguageDetect, '/api/v1/text')

if __name__ == '__main__':
    app.run(debug=True)
