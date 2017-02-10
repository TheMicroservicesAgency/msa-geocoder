from flask import Flask, jsonify, redirect
import reverse_geocoder as rg

app = Flask(__name__)


@app.route('/hello-world')
def hello_world():
    data = {'message': 'Hello, World!'}
    response = jsonify(data)
    return response

@app.route('/geocoder')
def geocoder():
    coordinates = (51.5214588,-0.1729636),(9.936033, 76.259952),(37.38605,-122.08385)
    results = rg.search(coordinates)
    response = jsonify(results)
    return response

if __name__ == "__main__":

    #app.run(debug=True, port=8080, threaded=True)
    app.run(port=8080, threaded=True)
