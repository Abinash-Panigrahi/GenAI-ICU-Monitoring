from google import genai
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_report(json_file_path="vitals_log.json"):
    with open(json_file_path, "r") as f:
        vitals = json.load(f)

    prompt = f"""
    You are a clinical assistant for ICU doctors.
    Generate a professional shift summary report based on the following vitals data.

    Vitals Data:
    {json.dumps(vitals, indent=2)}

    Format the report using markdown EXACTLY like this:

    ## 🏥 PATIENT MONITORING REPORT
    **Time:** [timestamp] | **Device:** [device_name]

    ---

    ### 📊 VITALS SNAPSHOT
    | Vital | Value | Status |
    |-------|-------|--------|
    | Heart Rate | [value] [unit] | ✅ Normal / ⚠️ Abnormal |
    | SpO2 | [value] [unit] | ✅ Normal / ⚠️ Abnormal |
    | Pulse Rate | [value] [unit] | ✅ Normal / ⚠️ Abnormal |
    | PI | [value] [unit] | ✅ Normal / ⚠️ Abnormal |
    | NIBP | [systolic]/[diastolic] [unit] | ✅ Normal / ⚠️ Abnormal |
    | Temperature T1 | [value] [unit] | ✅ Normal / ⚠️ Abnormal |
    | Temperature T2 | [value] [unit] | ✅ Normal / ⚠️ Abnormal |

    ---

    ### ⚠️ ALERTS & CONCERNS
    - [alert 1]
    - [alert 2]

    ---

    ### 📋 RECOMMENDATION
    [2-3 lines of clinical recommendation]

    **Next check recommended in:** [time]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )
    
    return response.text


def generate_quick_status(json_file_path="vitals_log.json"):
    with open(json_file_path, "r") as f:
        vitals = json.load(f)

    prompt = f"""
    You are a clinical assistant for ICU doctors.
    Based on the following vitals data, generate an extremely short one-line status.

    Vitals Data:
    {json.dumps(vitals, indent=2)}

    Format EXACTLY like this single line:
    [STATUS] | HR:[value][unit] | SpO2:[value]% | NIBP:[sys]/[dia]mmHg | Temp:[value]°C | [one short action if needed]

    Rules:
    - STATUS must be one of: 🟢 STABLE, 🟡 MONITOR, 🔴 CRITICAL
    - If value is null, write N/A
    - Keep entire output under 120 characters
    - No explanation, no extra text, just the one line
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )

    return response.text.strip()