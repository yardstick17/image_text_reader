# -*- coding: utf-8 -*-
import logging
import os
import tempfile

import requests
import werkzeug
from flask import Flask, jsonify
from flask import abort
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse

from read_image import read_image_from_file

ROOT_PATH = '/read_image_from_file'


class ReadViaImage(Resource):
    def post(self):
        file_ = parse_arg_from_requests(arg='image', type=werkzeug.FileStorage, location='files')
        if not file_:
            abort(400, "Required form-data param 'image' type=ImageFile")
        _setup()  # Loads model and weights - takes ~2 seconds
        file_descriptor, filename = tempfile.mkstemp(suffix='.jpg')
        logging.info('Saving file: %s', filename)
        file_.save(filename)
        text_in_image = read_image_and_delete(filename)
        return jsonify(status='success',
                       text_in_image=text_in_image.split('\n'),
                       version='0.0.1',
                       )


class ReadViaUrl(Resource):
    def post(self):
        url = parse_arg_from_requests(arg='url', type=str)
        if not url:
            abort(400, "Required form-data param 'url' type=string")
        _setup()  # Loads model and weights - takes ~2 seconds
        filename = download_image(url)
        text_in_image = read_image_and_delete(filename)
        return jsonify(status='success',
                       text_in_image=text_in_image.split('\n'),
                       version='0.0.1',
                       )


def read_image_and_delete(filename):
    logging.info('Hold on reading text')
    result = read_image_from_file(filename)
    print('read txt : \n', result)
    logging.info('Removing file: %s', filename)
    os.remove(filename)
    return result


def parse_arg_from_requests(arg, **kwargs):
    parse = reqparse.RequestParser()
    parse.add_argument(arg, **kwargs)
    args = parse.parse_args()
    return args[arg]


def download_image(url):
    logging.info('Downloading image from url: %s', url[:100])
    response_object = requests.get(url)
    file_descriptor, filename = tempfile.mkstemp()
    logging.info('Saving file: %s', filename)
    with open(file_descriptor, mode='wb') as code:
        code.write(response_object.content)
    return filename


def setup_api():
    api = Api(app)
    api.add_resource(ReadViaImage, ROOT_PATH + '/image')
    api.add_resource(ReadViaUrl, ROOT_PATH + '/url')


def _setup():
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s', level=logging.INFO)


app = Flask(__name__)
setup_api()

if __name__ == '__main__':
    _setup()
    app.run(debug=True, host='0.0.0.0', port=6600)
