from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_vitals(image_path):
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = """
    Look at this ICU monitor image and extract the vitals.
    Return ONLY a JSON object like this:
    {
        "heart_rate": 0,
        "spo2": 0,
        "blood_pressure_systolic": 0,
        "blood_pressure_diastolic": 0,
        "respiratory_rate": 0,
        "temperature": 0
    }
    If a value is not visible, use null.
    Return ONLY JSON, no explanation.
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