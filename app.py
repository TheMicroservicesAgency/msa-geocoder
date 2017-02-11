from flask import Flask, jsonify, request
import reverse_geocoder as rg

app = Flask(__name__)


@app.route('/geocoder')
def reverse_geocode():
    """Reverse-gecode (find the closest city of 1000+ habitants) from the given 
    latitude/longitude parameters"""

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if lat is None or lon is None:
        msg = {'ERROR': 'Missing parameter.'}
        return jsonify(msg), 400

    try:
        lat = float(lat)
    except ValueError:
        msg = {'ERROR': 'The specified latitude is not a number.'}
        return jsonify(msg), 400

    try:
        lon = float(lon)
    except ValueError:
        msg = {'ERROR': 'The specified longitude is not a number.'}
        return jsonify(msg), 400

    if lat < -90.0 or lat > 90.0:
        msg = {'ERROR': 'The specified latitude is invalid.'}
        return jsonify(msg), 400

    if lon < -180.0 or lon > 180.0:
        msg = {'ERROR': 'The specified longitude is invalid.'}
        return jsonify(msg), 400

    coordinates = (lat, lon)
    results = rg.search(coordinates)

    # Should only have one result
    response = jsonify(results[0])
    return response


@app.route('/geocoder', methods=['POST'])
def reverse_geocode_from_geojson():
    """Reverse-geocode the coordinates from a given geojson Point document"""

    try:
        data = request.json

        if data['type'] == 'Point':

            # Remember that geohash uses lat,lon
            # but geojson uses lon,lat
            lon = data['coordinates'][0]
            lat = data['coordinates'][1]

            coordinates = (lat, lon)
            results = rg.search(coordinates)

            # Should only have one result
            response = jsonify(results[0])
            return response

        else:
            msg = {'ERROR': 'Geojson type is not a Point'}
            return jsonify(msg), 400

    except Exception as e:
        print(e)
        msg = {'ERROR': 'Could not parse geojson.'}
        return jsonify(msg), 400


if __name__ == "__main__":

    app.run(port=8080, threaded=True)
