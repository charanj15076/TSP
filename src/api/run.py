import os
import psycopg2
import json
import datetime
from shapely import wkb
import pandas as pd
import geopandas as gpd

from dotenv import load_dotenv

import flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS

from services import solve_tsp

load_dotenv()

app = flask.Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# helper to object turn into json
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Home(Resource):
    def get(self):
        data = {
            "message" : "Hello! API is running!"
        }

        return {
            "data": data,
        }


class Run(Resource):
    # solve TSP given list of destinations
    def post(self):
        # args = request.args
        # destination_list = args['destination_list']
        # technique = args['technique']

        json_data = request.get_json(force=True)
        destination_list = json_data['destination_list']
        technique = json_data['technique']

        edge_list = solve_tsp(destination_list, technique) 

        routes_merged = gpd.GeoDataFrame( pd.concat( edge_list, ignore_index=True) )

        result = {
            "routes": routes_merged.to_json(),
        }

        return {
            "data": result,
            "status": "SUCCESS",
        }


api.add_resource(Home, "/")
api.add_resource(Run, "/run")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)