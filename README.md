
# msa-geocoder

Reverse geocoding as a simple offline service.

For a given latitude,longitude returns the matching country code, the administrative region and the name of the closest city (cities with population of 1000+). Data from the [GeoNames project](http://www.geonames.org/).

Built using [reverse-geocoder](https://github.com/thampiman/reverse-geocoder), an updated version of [reverse_geocode](https://pypi.python.org/pypi/reverse_geocode/1.0).

## Quick start

Execute the microservice container with the following command :

    docker run -ti -p 9908:80 msagency/msa-geocoder

## Examples

    $ curl "http://localhost:9908/geocoder?lat=45.5017&lon=-73.5673"
    {
      "admin1": "Quebec",
      "admin2": "Montreal",
      "cc": "CA",
      "lat": "45.50884",
      "lon": "-73.58781",
      "name": "Montreal"
    }

With a geojson Point :

    $ curl -X POST -H "Content-Type: application/json" "http://localhost:9908/geocoder" -d '{
      "coordinates": [
        15.087,
        37.503
      ],
      "type": "Point"
    }'

    {
      "admin1": "Sicily",
      "admin2": "Catania",
      "cc": "IT",
      "lat": "37.49223",
      "lon": "15.07041",
      "name": "Catania"
    }

## Endpoints

- GET [/geocoder?lat=XX.XX&lon=XX.XX](/geocoder?lat=45.536&lon=-73.620) : returns the location data for the given lat, lon
- POST [/geocoder]() : returns the location data for the given geojson Point

## Standard endpoints

- GET [/ms/version](/ms/version) : returns the version number
- GET [/ms/name](/ms/name) : returns the name
- GET [/ms/readme.md](/ms/readme.md) : returns the readme (this file)
- GET [/ms/readme.html](/ms/readme.html) : returns the readme as html
- GET [/swagger/swagger.json](/swagger/swagger.json) : returns the swagger api documentation
- GET [/swagger/#/](/swagger/#/) : returns swagger-ui displaying the api documentation
- GET [/nginx/stats.json](/nginx/stats.json) : returns stats about Nginx
- GET [/nginx/stats.html](/nginx/stats.html) : returns a dashboard displaying the stats from Nginx

## About

A project by the [Microservices Agency](http://microservices.agency).
