from pydantic import BaseModel, field_validator
from typing import Optional
import json


class VitalsModel(BaseModel):
    heart_rate: Optional[float] = None
    heart_rate_unit: Optional[str] = None
    spo2: Optional[float] = None
    spo2_unit: Optional[str] = None
    pulse_rate: Optional[float] = None
    pulse_rate_unit: Optional[str] = None
    pi: Optional[float] = None
    pi_unit: Optional[str] = None
    nibp_systolic: Optional[float] = None
    nibp_diastolic: Optional[float] = None
    nibp_unit: Optional[str] = None
    nibp_status: Optional[str] = None
    temperature_t1: Optional[float] = None
    temperature_t1_unit: Optional[str] = None
    temperature_t2: Optional[float] = None
    temperature_t2_unit: Optional[str] = None
    ecg_status: Optional[str] = None
    patient_mode: Optional[str] = None
    operation_speed: Optional[str] = None
    waveform_type: Optional[str] = None
    device_name: Optional[str] = None
    timestamp: Optional[str] = None
    alarm_status: Optional[str] = None
    any_other_visible_data: Optional[str] = None

    @field_validator("heart_rate")
    def check_heart_rate(cls, v):
        if v is not None and not (20 <= v <= 300):
            return None
        return v

    @field_validator("spo2")
    def check_spo2(cls, v):
        if v is not None and not (50 <= v <= 100):
            return None
        return v

    @field_validator("pulse_rate")
    def check_pulse_rate(cls, v):
        if v is not None and not (20 <= v <= 300):
            return None
        return v

    @field_validator("pi")
    def check_pi(cls, v):
        if v is not None and not (0 <= v <= 20):
            return None
        return v

    @field_validator("nibp_systolic")
    def check_nibp_systolic(cls, v):
        if v is not None and not (40 <= v <= 300):
            return None
        return v

    @field_validator("nibp_diastolic")
    def check_nibp_diastolic(cls, v):
        if v is not None and not (20 <= v <= 200):
            return None
        return v

    @field_validator("temperature_t1", "temperature_t2")
    def check_temperature(cls, v):
        if v is not None and not (25 <= v <= 45):
            return None
        return v


def validate_vitals(raw_data: dict):
    try:
        validated = VitalsModel(**raw_data)
        return validated.model_dump()
    except Exception as e:
        print(f"Validation error: {e}")
        return raw_data


def save_to_file(vitals: dict, file_path="vitals_log.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(vitals, f, indent=4)
        print("Vitals saved to file")
    except Exception as e:
        print(f"File save error: {e}")