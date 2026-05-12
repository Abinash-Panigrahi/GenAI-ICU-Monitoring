# pyrefly: ignore [missing-import]
from supabase import create_client
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os

load_dotenv()

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def save_to_db(vitals: dict):
    try:
        data = {
            "heart_rate": vitals.get("heart_rate"),
            "heart_rate_unit": vitals.get("heart_rate_unit"),
            "spo2": vitals.get("spo2"),
            "spo2_unit": vitals.get("spo2_unit"),
            "pulse_rate": vitals.get("pulse_rate"),
            "nibp_systolic": vitals.get("nibp_systolic"),
            "nibp_diastolic": vitals.get("nibp_diastolic"),
            "temperature_t1": vitals.get("temperature_t1"),
            "temperature_t2": vitals.get("temperature_t2"),
            "ecg_status": vitals.get("ecg_status"),
            "device_name": vitals.get("device_name"),
            "timestamp": vitals.get("timestamp"),
            "alarm_status": vitals.get("alarm_status"),
        }

        client.table("vitals").insert(data).execute()
        print("Saved to database")

    except Exception as e:
        print(f"Database error: {e}")