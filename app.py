from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from letter_boxed import letter_boxed_solver
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)


class LetterBoxed(Resource):
    @cross_origin()
    def get(self): # parameters in query: words_file, allowed_letters, debug, find_all_solutions
        words_file = request.args.get('words_file')
        allowed_letters = request.args.get('allowed_letters')
        find_all_solutions = request.args.get('find_all_solutions')
        debug = request.args.get('debug')
        solutions = letter_boxed_solver(words_file, allowed_letters, find_all_solutions, debug)
        return jsonify(solutions)

api.add_resource(LetterBoxed, '/')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5001)