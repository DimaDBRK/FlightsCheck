from flask import Flask, request, Response, jsonify, Blueprint
from flask_cors import CORS, cross_origin
from operator import itemgetter
from config import Config
import os

# functions
from functions import search_flight
from functions import parse_flights_info_from_file
from functions import expensive_flight
from functions import cheapest_flight 
from functions import fastest_flight 
from functions import longest_flight
from functions import optimal_flight

app = Flask(__name__)
CORS(app)  # ADD ALLOWED ORIGIN LIST LATER
app.config.from_object(Config)

"""
BEGIN FLIGHT ROUTES
"""
bp_flight = Blueprint("flight", __name__, url_prefix="/flight")


@bp_flight.route("/options", methods=["GET"])
def options():
  print("flight/options")
  # request => ?source=NYC&destination=LA
  # Retrieve 'source' and 'destination' from the request's query parameters
  try:
    source = request.args.get('source')
    destination = request.args.get('destination')
    print(source, destination)
    if not source or not destination:
      return jsonify({"msg": "Request problem. No source or destination"}), 500
    
    # for file "RS_Via-3.xml" => both directions
    # flights_info_both  = parse_flights_info_from_file("RS_Via-3.xml")
    
    # for file "RS_ViaOW.xml" => only onward
    flights_info_onward = parse_flights_info_from_file("RS_ViaOW.xml")

    if not flights_info_onward:
       return jsonify({"msg": "Internal error. No xml file found."}), 500
    # parse_flights_info_from_file
    res = search_flight(source, destination, flights_info_onward)
          
    return jsonify(res), 200
  
  except Exception as e:
    print(e)
    return jsonify({"msg": "An error occurred"}), 500
  
  
@bp_flight.route("/analysis", methods=["GET"])
def analysis():
  print("flight/analysis")
  # request => ?source=NYC&destination=LA
  # Retrieve 'source' and 'destination' from the request's query parameters
  try:
    source = request.args.get('source')
    destination = request.args.get('destination')
    print(source, destination)
    if not source or not destination:
      return jsonify({"msg": "Request problem. No source or destination"}), 500
    
    # for file "RS_Via-3.xml" => both directions
    # flights_info_both  = parse_flights_info_from_file("RS_Via-3.xml")
    
     # for file "RS_ViaOW.xml" => only onward
    flights_info_onward = parse_flights_info_from_file("RS_ViaOW.xml")
    
    if not flights_info_onward:
       return jsonify({"msg": "Internal error. No xml file found."}), 500
    
    # get all flights
    flights = search_flight(source, destination, flights_info_onward)
    
    expensive = expensive_flight(flights)
    cheapest = cheapest_flight(flights)
    fastest = fastest_flight(flights)
    longest = longest_flight(flights)
    optimal = optimal_flight(flights)
    
    res = {
      "expensive": expensive,
      "cheapest": cheapest,
      "fastest": fastest,
      "longest": longest,
      "optimal": optimal
    }
    
    return jsonify(res), 200
  
  except Exception as e:
    print(e)
    return jsonify({"msg": "An error occurred"}), 500


app.register_blueprint(bp_flight)
     
"""
END FLIGHT ROUTES
"""