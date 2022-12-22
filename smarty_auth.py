import os

from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup

def smarty_auth(address):
	auth_id = "5a8ac2e1-59cb-f0ec-1780-f160367cbce9"
	auth_token = "hesJ4dcS0DrZjHN73CGg"

	credentials = StaticCredentials(auth_id, auth_token)

	client = ClientBuilder(credentials).build_us_street_api_client()
	# client = ClientBuilder(credentials).with_proxy('localhost:8080', 'user', 'password').build_us_street_api_client()
	# Uncomment the line above to try it with a proxy instead

	# Documentation for input fields can be found at:
	# https://www.smarty.com/docs/us-street-api#input-fields

	lookup = Lookup()
	lookup.street = address["st_and_apt"]
	lookup.city = address["city"]
	lookup.state = address["state"]
	lookup.country = address["country"]
	lookup.zipcode = address["zipcode"]

	try:
		client.send_lookup(lookup)
	except exceptions.SmartyException as err:
		print(err)
		return

	result = lookup.result

	if not result:
		print("No candidates. This means the address is not valid.")
		return False

	print("Address is valid. (There is at least one candidate)\n")
	return True

	# first_candidate = result[0]

	# print("Address is valid. (There is at least one candidate)\n")
	# print("Delivery Information")
	# print("--------------------")
	# print("Delivery line 1: {}".format(first_candidate.delivery_line_1))
	# print("Delivery line 2: {}".format(first_candidate.delivery_line_2))
	# print("Last line:	    {}".format(first_candidate.last_line))
	# print()

	# print("Address Components")
	# print("-------------------")
	# print("Primary number:  {}".format(first_candidate.components.primary_number))
	# print("Predirection:	{}".format(first_candidate.components.street_predirection))
	# print("Street name:	    {}".format(first_candidate.components.street_name))
	# print("Street suffix:   {}".format(first_candidate.components.street_suffix))
	# print("Postdirection:   {}".format(first_candidate.components.street_postdirection))
	# print("City:			{}".format(first_candidate.components.city_name))
	# print("State:		    {}".format(first_candidate.components.state_abbreviation))
	# print("ZIP Code:		{}".format(first_candidate.components.zipcode))
	# print("County:		    {}".format(first_candidate.metadata.county_name))
	# print("Latitude:		{}".format(first_candidate.metadata.latitude))
	# print("Longitude:	    {}".format(first_candidate.metadata.longitude))
    