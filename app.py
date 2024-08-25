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
        print(allowed_letters)
        find_all_solutions = request.args.get('find_all_solutions') == 'true'
        debug = request.args.get('debug') == 'true'
        limit = request.args.get('limit')

        solutions = letter_boxed_solver(words_file, allowed_letters, find_all_solutions, debug, limit)
        print("Solutions: ", len(solutions))
        return jsonify(solutions)

api.add_resource(LetterBoxed, '/')

if __name__ == '__main__':
    from waitress import serve
    print("Now serving")

    app.run(port=5000) # use flask run --host=0.0.0.0 instead of setting context or url_scheme
