import os
import time
import pyEX as p
import Data as data
from settings import load_config
from flask import Flask
from queue import Queue
from flask_jsonpify import jsonify
from flask_restful import Resource, Api

# define globals to keep the state
q1_size = -1
q1 = Queue(maxsize=1)
array = []
symbols = None

app = Flask(__name__)
api = Api(app)


class Reset(Resource):
    @staticmethod
    def get():
        global symbols
        global q1_size
        global array
        symbols = None
        q1_size = -1
        array = []
        return jsonify('Success')


class GetSymbols(Resource):
    @staticmethod
    def get(num):
        # Maintain the state
        global q1_size
        global q1
        global array
        global symbols

        # Can move to a pub/sub message implementation where assignments are pushed and nodes consume
        while q1.full():
            time.sleep(5)

        q1.put(num)
        q1_size += 1
        if symbols is None:
            c = p.Client(version='v1', api_limit=0)
            syms = c.symbolsList()

            for group in data.chunker(syms, int(num)):
                array.append(group)

        result = array[q1_size]
        q1.get()
        return jsonify(result)


api.add_resource(Reset, '/reset')
api.add_resource(GetSymbols, '/symbols/<num>')

if __name__ == '__main__':
    load_config()
    q = Queue(maxsize=1)
    app.run(host='0.0.0.0', port=os.environ["PORT"])
