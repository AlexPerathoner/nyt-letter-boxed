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
#    serve(app, host="0.0.0.0", port=5000, url_scheme='https')

    context = ('/etc/letsencrypt/live/nytalexpera.duckdns.org/fullchain.pem', '/etc/letsencrypt/live/nytalexpera.duckdns.org/privkey.pem') # certificate and key files
    app.run(host='192.168.0.197', port=5000) #, ssl_context=context) # use flask run --host=0.0.0.0 instead
