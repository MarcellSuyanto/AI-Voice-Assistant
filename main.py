print("Starting up Libraries...\n")

from vapi import Vapi
from vapi.core.api_error import ApiError
import os
from dotenv import load_dotenv
import time

print("Fetching environment variables...\n")
load_dotenv()


auth_token = os.getenv("VAPI_API_KEY")
if not auth_token:
    raise ValueError("VAPI_API_KEY not set")

phone_number_id = os.getenv("PHONE_NUMBER")  
if not phone_number_id:
    raise ValueError("PHONE_NUMBER not set")

customer_number = os.getenv("MY_PHONE_NUMBER")
if not customer_number:
    raise ValueError("MY_PHONE_NUMBER not set")

assistant_ID = os.getenv("ASSISTANT_ID")
if not assistant_ID:
    raise ValueError("ASSISTANT_ID not set")

print("Environment variables loaded successfully.\n")

# Initialize VAPI client
client = Vapi(token=auth_token)

def wait_for_call_end(client, call_id, timeout=300):
    """Wait until the call reaches 'ended' status or timeout."""
    start_time = time.time()
    last_status = None
    current_status = None
    while current_status != "ended":
        try:
            call = client.calls.get(call_id)
            current_status = call.status
            if current_status == "ended":
                print("Call ended.\n")
                return True
            
            if current_status != last_status:
                print(f"Call Status: {current_status}")  

            elif current_status in ["failed", "no-answer"]:
                print(f"Call terminated with status: {current_status}")
                return False
            last_status = current_status

        except ApiError as e:
            print(f"API Error: {e}")
            return False
        time.sleep(5)
    print("Timeout: Call did not end within the expected time.")
    return False
try:
    # Start the call
    print("Starting call...")
    call = client.calls.create(
        assistant_id=assistant_ID,
        phone_number={
            "twilioPhoneNumber": phone_number_id,
            "twilioAccountSid": os.getenv("TWILIO_ACCOUNT_SID"),
            "twilioAuthToken": os.getenv("TWILIO_AUTH_TOKEN")
        },
        customer={"number": customer_number}
    )
    print(f"Call ID: {call.id}\n")

    def get_call_data(client, call_id):
        """Fetch call data, retrying if analysis isn't ready yet."""
        print("Fetching data...")
        time.sleep(10)
        metadata = client.calls.get(call_id)

        summary = metadata.analysis.summary
        transcript = metadata.artifact.transcript
        success =  metadata.analysis.success_evaluation

        return {
            'summary': summary,
            'transcript': transcript,
            'success': success,
        }


    # Wait for call to finish
    if wait_for_call_end(client, call.id):
        # Fetch data 
        analysis = get_call_data(client, call.id)
        if analysis:
            with open("Summary.txt", "w") as f:
                f.write(f"Summary: \n{analysis['summary']}\n")
                f.write("\n")
                f.write(f"Success: {analysis['success']}\n")
                f.write("\n")
            print("Data saved successfully!")
            with open("Transcript.txt", "w") as f:
                f.write(f"Transcript: \n{analysis['transcript']}\n")
                f.write("\n")
        else:
            print("Failed to retrieve call analysis data.")
    else:
        print("Call did not complete properly.")

except ApiError as e:
    print(f"API Error: {e.status_code} - {e.body}")
except Exception as e:
    print(f"Unexpected error: {e}") 
