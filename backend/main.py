# parser functions test

import xml.etree.ElementTree as ET
import os 
from datetime import datetime
from typing import List, Dict

# settings
dir_path = os.path.dirname(os.path.realpath(__file__))

# date time format
date_format = '%Y-%m-%dT%H%M'

# duration
def flight_duration_from_string_format(departure_str, arrival_str):
  departure= datetime.strptime(departure_str, date_format )
  arrival= datetime.strptime(arrival_str, date_format)
  duration = arrival - departure
  return duration.total_seconds()

# functions
def root_data_from_xml_file (file_name):
  # import data by reading from a file
  data = ET.parse(f'{dir_path}/data/{file_name}')
  # root type Element
  root = data.getroot()
  return root

def parse_flights_info_from_file(file_name):
  
  # function to parse one flights element
  
  root = root_data_from_xml_file(file_name)
 
  # list to store info
  flights_info = []
  # print("test=>", root.findall('./PricedItineraries'))
  for element in root.findall('./PricedItineraries/Flights'):

    # element pricing, check element lenth
    pricing = element.find('Pricing')
    currency = pricing.attrib["currency"]
    pricing_type = pricing[0].attrib["type"]
    pricing_base_fare = pricing[0].text
    airline_taxes = pricing[1].text
    total_amount = pricing[2].text
    
  # element => OnwardPricedItinerary
    direction = element[0].tag
    for x in element[0][0]:
      flight_data = {
        'Direction': direction,
        'CarrierId': x.find('Carrier').attrib['id'],
        'Carrier': x.find('Carrier').text,
        'FlightNumber': x.find('FlightNumber').text,
        'Source': x.find('Source').text,
        'Destination': x.find('Destination').text,
        'DepartureTimeStamp': x.find('DepartureTimeStamp').text, 
        'ArrivalTimeStamp': x.find('ArrivalTimeStamp').text,
        'Duration': flight_duration_from_string_format(x.find('DepartureTimeStamp').text, x.find('ArrivalTimeStamp').text),
        'Class': x.find('Class').text,
        'NumberOfStops': x.find('NumberOfStops').text,
        'FareBasis': x.find('FareBasis').text.strip(),
        'TicketType': x.find('TicketType').text,
        'Currency': currency,
        'PricingType': pricing_type,
        'PricingBaseFare': pricing_base_fare,
        'AirlineTaxes': airline_taxes,
        'TotalAmount': total_amount
      }
      
      flights_info.append(flight_data)
    # element => ReturnPricedItinerary. Check if exist
    if len(element) > 2:
      direction = element[1].tag
      
      for x in element[1][0]:
        flight_data = {
          'Direction': direction,
          'CarrierId': x.find('Carrier').attrib['id'],
          'Carrier': x.find('Carrier').text,
          'FlightNumber': x.find('FlightNumber').text,
          'Source': x.find('Source').text,
          'Destination': x.find('Destination').text,
          'DepartureTimeStamp': x.find('DepartureTimeStamp').text,
          'ArrivalTimeStamp': x.find('ArrivalTimeStamp').text,
          'Duration': flight_duration_from_string_format(x.find('DepartureTimeStamp').text, x.find('ArrivalTimeStamp').text),
          'Class': x.find('Class').text,
          'NumberOfStops': x.find('NumberOfStops').text,
          'FareBasis': x.find('FareBasis').text.strip(),
          'TicketType': x.find('TicketType').text,
          'Currency': currency,
          'PricingType': pricing_type,
          'PricingBaseFare': pricing_base_fare,
          'AirlineTaxes': airline_taxes,
          'TotalAmount': total_amount
        }
        
        flights_info.append(flight_data)
 
  return flights_info

# search fligth with source and destination
def search_flight(source, destination, flight_info_list, direction = 'OnwardPricedItinerary'):
  return [element for element in flight_info_list if element['Source'] == source and element['Destination'] == destination and element['Direction'] == direction ] 

# convert txt airport code to list of dictionaries and store to file
def airport_codes_from_txt(file_name="text.txt"):
  file_path = f'{dir_path}/data/{file_name}'
  airports = []

  with open(file_path, 'r', encoding='utf-8') as file:
      for line in file:
          parts = line.strip().split('\t')
          if len(parts) == 3:
              airport = {
                  "code": parts[0],
                  "name": parts[1],
                  "country": parts[2]
              }
              airports.append(airport)

  return airports

  
# analysis - the most expensive, cheapest, fastest, longest, and optimal flight options
def expensive_flight(flights_list: List[Dict]) -> List[Dict]:
  """
  Find the expensive flights in a list of flight information dictionaries.
  Args: flight_list (List[Dict]): A list of dictionaries, each representing flight information.
  Returns: List[Dict]: A list of dictionaries representing results.
  """
  # list to hold the result
  flights = []
  
  # find the max price = target from the list of flights by "TotalAmount". Convert str to float
  target_price = max(float(flight['TotalAmount']) for flight in flights_list)
  
  # collect all the flights that have target price
  flights = [flight for flight in flights_list if float(flight['TotalAmount']) == target_price]
  
  return flights


def cheapest_flight(flights_list: List[Dict]) -> List[Dict]:
  """
  Find the cheapest flights in a list of flight information dictionaries.
  Args: flight_list (List[Dict]): A list of dictionaries, each representing flight information.
  Returns: List[Dict]: A list of dictionaries representing results.
  """
  # list to hold the result
  flights = []
  
  # find the min price = target from the list of flights by "TotalAmount". Convert str to float
  target_price = min(float(flight['TotalAmount']) for flight in flights_list)
  
  # collect all the flights that have target price
  flights = [flight for flight in flights_list if float(flight['TotalAmount']) == target_price]
  
  return flights

def fastest_flight(flights_list: List[Dict]) -> List[Dict]:
  """
  Find the fastest flights in a list of flight information dictionaries.
  Args: flight_list (List[Dict]): A list of dictionaries, each representing flight information.
  Returns: List[Dict]: A list of dictionaries representing results.
  """
  # list to hold the result
  flights = []
  
  # find the min duration = target from the list of flights 
  target_duration = min((flight_duration_from_string_format(flight["DepartureTimeStamp"], flight["ArrivalTimeStamp"])) for flight in flights_list)
  
  # collect all the flights that have target price
  flights = [flight for flight in flights_list if (flight_duration_from_string_format(flight["DepartureTimeStamp"], flight["ArrivalTimeStamp"])) == target_duration]
  
  return flights

def longest_flight(flights_list: List[Dict]) -> List[Dict]:
  """
  Find the fastest flights in a list of flight information dictionaries.
  Args: flight_list (List[Dict]): A list of dictionaries, each representing flight information.
  Returns: List[Dict]: A list of dictionaries representing results.
  """
  # list to hold the result
  flights = []
  
  # find the max duration = target from the list of flights 
  target_duration = max((flight_duration_from_string_format(flight["DepartureTimeStamp"], flight["ArrivalTimeStamp"])) for flight in flights_list)
  
  # collect all the flights that have target price
  flights = [flight for flight in flights_list if (flight_duration_from_string_format(flight["DepartureTimeStamp"], flight["ArrivalTimeStamp"])) == target_duration]
  
  return flights


def optimal_flight(flights_list: List[Dict]) -> List[Dict]:
  """
  Find the optimal flights in a list of flight information dictionaries.
  morning_departure - criteria that favors flights departing between 5 am to 10 am
  
  Args: flight_list (List[Dict]): A list of dictionaries, each representing flight information.
  Returns: List[Dict]: A list of dictionaries representing results.
  """
  # list to hold the result
  flights = []
  
  if not flights_list or len(flights_list) == 0:
        return None
  # criteria 
  criteria_weights = {"TotalAmount": 0.6, "Duration": 0.3, "NumberOfStops": -0.1, "Morning": 0.2}
  
  # normalize cost and duration
  max_amount = float(max(flights_list, key=lambda flight: float(flight.get("TotalAmount", 0)))["TotalAmount"])
  max_duration = float(max(flights_list, key=lambda flight: float(flight.get("Duration", 0)))["Duration"])
   
  
  
 
  # find optimal = target from the list of flights => sort based on optimization criteria
  flights = sorted(flights_list, key=lambda flight: (
    float(flight.get("TotalAmount", 0)) * criteria_weights.get("TotalAmount", 1) / ((lambda x: 1 if x == 0 else x)(max_amount)),
    flight_duration_from_string_format(flight["DepartureTimeStamp"], flight["ArrivalTimeStamp"]) * criteria_weights.get("Duration", 1) / ((lambda x: 1 if x == 0 else x)(max_duration)),
    float(flight.get("NumberOfStops", 0)) * criteria_weights.get("NumberOfStops", 1),
    (0 if 5 <= datetime.strptime(flight["DepartureTimeStamp"], date_format).hour <= 10 else 1) * criteria_weights.get("Morning", 1)  # Morning departure check
    )
  )
   
  return flights[0]


# Driver

# airport codes
airport_codes = airport_codes_from_txt()
# for file "RS_Via-3.xml" => both directions
flights_info_both  = parse_flights_info_from_file("RS_Via-3.xml")
# for file "RS_ViaOW.xml" => only onward
flights_info_onward = parse_flights_info_from_file("RS_ViaOW.xml")


# find flights from to 
filtered_flights = search_flight("DXB", "BKK", flights_info_both)
print(filtered_flights)
filtered_flights_onward = search_flight("DXB", "BKK", flights_info_onward)


# print("expensive", expensive_flight(filtered_flights))
# print("cheapest", cheapest_flight(filtered_flights))
# print("fastest", fastest_flight(filtered_flights))
# print("longest", longest_flight(filtered_flights))

# print("optimal", optimal_flight(filtered_flights))

# Find the differences (elements present in list1 but not in list2)
differences = [item for item in filtered_flights if item not in filtered_flights_onward]

# print("Differences:", differences)