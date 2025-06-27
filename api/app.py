# GLORY BE TO GOD,
# PHONE NUMBER VALIDATION API,
# BY ISRAEL MAFABI EMMANUEL

from flask import Flask, request, jsonify
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import os

# initializing the flask application
app = Flask(__name__)

# configurations
RAPIDAPI_PROXY_SECRET:str|None = os.environ.get('RAPIDAPI_PROXY_SECRET')

# security helper function
# we are checking if the request is authorized by RapidAPI
def check_rapidapi_secret():
    """
    Operation:
    - Checks for RapidAPI Proxy Secret.
    - Returns None if the check passes.
    - Returns a Flask response tuple (json, status_code) if the check fails.
    """
    # acknowledging that the check is crucial.
    # the server should not run if the secret is not configured.
    if not RAPIDAPI_PROXY_SECRET:
        print(f"CRITICAL SERVER ERROR: RAPIDAPI_PROXY_SECRET is not set. Halting Request.")
        return jsonify({"error": "API misconfiguration, please contact support(mafabi_israel@outlook.com)"}), 500
    
    # Get the secret sent by the RapidAPI proxy
    incoming_secret:str|None = request.headers.get('X-RapidAPI-Proxy-Secret')

    # check if the incoming secret matches the expected secret
    if not incoming_secret or incoming_secret != RAPIDAPI_PROXY_SECRET:
        # if the secret is missing or does not match, return an authorization error (unauthorized)
        return jsonify({"error": f"Unauthorized: Invalid or missing API Credentials."}), 401
    
    # otherwise the secret is valid, return None to signal success
    return None


# our code endpoint, validating the shared phone number
@app.route('/validate', methods=['GET'])
def validate_phone():
    """
    Operations:
    - Receives the shared phone number (provided as a query parameter), format (.../validate?number=+254743968877).
    - Then returns the validation information.
    """
    # 1. First, we run our security check.
    auth_error = check_rapidapi_secret()
    if auth_error:
        # if authentication fails, return the authentication failure information
        return auth_error
    
    # 2. If security passes, let's proceed with the main validation logic.
    phone_number_str:str|None = request.args.get('number')
    if not phone_number_str:
        return jsonify({"error": "Missing required parameter: 'number'"}), 400

    # Robustness... 
    # if the number starts with a space from a + in the url,
    # let's return the character, for it's needed in determining the country code...
    if phone_number_str.startswith(' '):
        phone_number_str = '+' + phone_number_str[1:]
    
    try:
        parsed_number = phonenumbers.parse(phone_number_str)
        is_valid = phonenumbers.is_valid_number(parsed_number)

        response_data:dict = { # type: ignore
            "input_number": phone_number_str,
            "is_valid": is_valid
        }

        if is_valid:
            # if the phone number is valid, lets add more details about it...
            response_data.update({ # type: ignore
                "country_code"        : parsed_number.country_code,
                "national_number"     : str(parsed_number.national_number),
                "e164_format"         : phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
                "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national_format"     : phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "location"            : geocoder.description_for_number(parsed_number, "en"),
                "carrier"             : carrier.name_for_number(parsed_number, "en") or "N/A",
                "timezones"           : timezone.time_zones_for_number(parsed_number) or []
            })
        else:
            # validation failed, like the phone is not legit...
            response_data["reason"] = "The provided phone number is not a valid or recognized phone number format."
            
        # we'll log the request for monitoring, just for now (development)
        print(f"Request for number '{phone_number_str}', Valid: {is_valid}")
        return jsonify(response_data), 200
    except phonenumbers.NumberParseException as e:
        return jsonify({"error": f"Could not parse phone number, Ensure it includes a country code. Details: {e.args[0]}"}), 400
    except Exception as e:
        print(f"An unexpected server error occurred: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


# health check endpoint
# it's vital for deployment and monitoring, we'll update in future.
# it doesn't need security
@app.route('/health', methods=['GET'])
def health_check():
    """
    Operations:
    - Confirms if the API is operational, running.
    """
    return jsonify({"status": "healthy"}), 200


# development server
if __name__ == '__main__':
    # for development,
    app.run(debug=True, port=5000)