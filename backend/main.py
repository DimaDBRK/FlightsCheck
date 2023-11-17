# parser functions test

import xml.etree.ElementTree as ET
import os 

# tests
dir_path = os.path.dirname(os.path.realpath(__file__))

# import data by reading from a file
file1 = ET.parse(f'{dir_path}/data/RS_Via-3.xml')
# root type Element
root = file1.getroot()
print("root=>", root)
print("root.tag=>", root.tag)
print("root.attrib=>", root.attrib)
print("root.attrib=>", root.attrib["ResponseTime"])

# list to store info
flights_info = []
# print("test=>", root.findall('./PricedItineraries'))
for element in root.findall('./PricedItineraries/Flights'):

  # element pricing
  currency = element[2].attrib["currency"]
  pricing_type = element[2][0].attrib["type"]
  pricing_base_fare = element[2][0].text
  airline_taxes = element[2][1].text
  total_amount = element[2][2].text
  
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
  # element => ReturnPricedItinerary
  
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
  
print(flights_info)