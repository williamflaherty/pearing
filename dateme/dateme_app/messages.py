# this file is a glorified txt list
def get_error_message(status_code):
	
	errors = {
		#01XX - Authorization
		"0100": "Unauthorized access to the Pearing API.",
		"0101": "This user failed Instagram's authorization.",

		#02XX - Username database violations
		"0200": "More than one user with this username in the database.",
		"0201": "The given username is already taken.",
		"0202": "The given username does not exist in the database",
	}

	code = status_code[:4]
	return errors[code]

