from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_vitals(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    This is an ICU patient monitor screen. Extract ALL visible data from it.
    Return ONLY a JSON object with these fields:
    {
        "heart_rate": null,
        "heart_rate_unit": null,
        "spo2": null,
        "spo2_unit": null,
        "pulse_rate": null,
        "pulse_rate_unit": null,
        "pi": null,
        "pi_unit": null,
        "nibp_systolic": null,
        "nibp_diastolic": null,
        "nibp_unit": null,
        "nibp_status": null,
        "temperature_t1": null,
        "temperature_t1_unit": null,
        "temperature_t2": null,
        "temperature_t2_unit": null,
        "ecg_status": null,
        "patient_mode": null,
        "operation_speed": null,
        "waveform_type": null,
        "device_name": null,
        "timestamp": null,
        "alarm_status": null,
        "any_other_visible_data": null
    }
    Rules:
    - If value is visible and readable, extract it exactly as shown
    - If value shows dashes (--), set as null
    - If value is unclear or not visible, set as null
    - Extract units separately (bpm, %, mmHg, C, F etc.)
    - Return ONLY JSON, no explanation, no extra text
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        ]
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)