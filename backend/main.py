'''from flask import Flask, request, jsonify
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

AGORA_APP_ID = os.getenv("AGORA_APP_ID")
AGORA_APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

from src.RtcTokenBuilder2 import *

def main():
    # Get the value of the environment variable AGORA_APP_ID. Make sure you set this variable to the App ID you obtained from Agora console.
    app_id = os.environ.get("AGORA_APP_ID")
    # Get the value of the environment variable AGORA_APP_CERTIFICATE. Make sure you set this variable to the App certificate you obtained from Agora console
    app_certificate = os.environ.get("AGORA_APP_CERTIFICATE")
    # Replace channelName with the name of the channel you want to join
    channel_name = input("Enter the channel name: ")
    # Fill in your actual user ID
    uid = input("Enter the user ID: ")
    # Token validity time in seconds
    token_expiration_in_seconds = 3600
    # The validity time of all permissions in seconds
    privilege_expiration_in_seconds = 3600

    print("App Id: %s" % app_id)
    print("App Certificate: %s" % app_certificate)
    if not app_id or not app_certificate:
        print("Need to set environment variable AGORA_APP_ID and AGORA_APP_CERTIFICATE")
        return

    # Generate Token
    token = RtcTokenBuilder.build_token_with_uid(app_id, app_certificate, channel_name, uid, Role_Subscriber,
                                                 token_expiration_in_seconds, privilege_expiration_in_seconds)
    print("Token: %s" % token)

if __name__ == "__main__":
    main()'''

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables
load_dotenv()

from src.RtcTokenBuilder2 import RtcTokenBuilder, Role_Subscriber

app = Flask(__name__)

CORS(app)

AGORA_APP_ID = os.getenv("AGORA_APP_ID")
AGORA_APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

if not AGORA_APP_ID or not AGORA_APP_CERTIFICATE:
    raise EnvironmentError("Please set AGORA_APP_ID and AGORA_APP_CERTIFICATE in your environment or .env file.")

@app.route("/generate_token", methods=["POST"])
def generate_token():
    """
    Expects JSON body:
    {
        "channel_name": "myChannel",
        "uid": "12345"
    }
    Returns:
    {
        "token": "generated_token_here"
    }
    """
    data = request.get_json()

    channel_name = data.get("channel_name")
    uid = data.get("uid")

    if not channel_name or not uid:
        return jsonify({"error": "Missing channel_name or uid"}), 400

    token_expiration_in_seconds = 3600
    privilege_expiration_in_seconds = 3600

    try:
        token = RtcTokenBuilder.build_token_with_uid(
            AGORA_APP_ID,
            AGORA_APP_CERTIFICATE,
            channel_name,
            uid,
            Role_Subscriber,
            token_expiration_in_seconds,
            privilege_expiration_in_seconds
        )
        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
