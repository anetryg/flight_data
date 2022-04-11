## Flight data
Python script, that for a given flight data in a form of csv file, prints out a structured list of all flight combinations for a selected route between airports A -> B, sorted by the final price for the trip.



## How to Use
The script is run from the command line, where the first argument is data in csv format, the second starting airport and the third end airport. For example:

python C:\Users\kiwi_fligh_data.py C:\Users\data.csv "DHE" "NIZ"



## Output
List of all flight combinations for a selected route between airports. Example:
[{'flights': 
	[{	'flight_no': 'WM263', 
		'origin': 'DHE', 
		'destination': 'NRX', 
		'departure': '2021-09-01T15:15:00', 
		'arrival': '2021-09-01T17:50:00', 
		'base_price': '70.0', 
		'bag_price': '12', 
		'bags_allowed': '1'}], 
	'bags_allowed': 1, 
	'destination': 'NIZ', 
	'origin': 'DHE', 
	'total_price': 121.0, 
	'travel_time': '2:00'}]
