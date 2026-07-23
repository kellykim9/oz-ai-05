from fastapi import APIRouter, HTTPException, UploadFile, File, Form, status
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import shutil

router = APIRouter(tags=["Patient & Medical Records"])

# 임시 데이터베이스 (메모리 저장소용)
fake_patients_db = []
fake_records_db = []

# 업로드된 X-ray 이미지가 저장될 기본 경로 설정
MEDIA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "media" / "xrays"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# --- Pydantic 스키마 ---
class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None


# --- 1. 환자 관리 (Patient) API ---

@router.post("/", status_code=status.HTTP_201_CREATED, summary="환자 정보 등록")
def create_patient(patient: PatientCreate):
    patient_id = len(fake_patients_db) + 1
    new_patient = {"id": patient_id, **patient.dict()}
    fake_patients_db.append(new_patient)
    return {"message": "환자가 성공적으로 등록되었습니다.", "data": new_patient}

@router.get("/", summary="환자 목록 조회")
def get_patients(name: Optional[str] = None):
    if name:
        return [p for p in fake_patients_db if name in p["name"]]
    return fake_patients_db

@router.get("/{patient_id}", summary="환자 상세 조회")
def get_patient(patient_id: int):
    for patient in fake_patients_db:
        if patient["id"] == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")

@router.put("/{patient_id}", summary="환자 정보 수정")
def update_patient(patient_id: int, patient_update: PatientUpdate):
    for patient in fake_patients_db:
        if patient["id"] == patient_id:
            if patient_update.name:
                patient["name"] = patient_update.name
            if patient_update.phone:
                patient["phone"] = patient_update.phone
            return {"message": "환자 정보가 수정되었습니다.", "data": patient}
    raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")

@router.delete("/{patient_id}", summary="환자 정보 삭제")
def delete_patient(patient_id: int):
    for index, patient in enumerate(fake_patients_db):
        if patient["id"] == patient_id:
            del fake_patients_db[index]
            return {"message": "환자 정보가 삭제되었습니다."}
    raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다.")


# --- 2. 진료기록 및 X-ray 업로드 API ---

@router.post("/records", status_code=status.HTTP_201_CREATED, summary="진료기록 및 X-ray 업로드")
def create_medical_record(
    patient_id: int = Form(...),
    chart_number: str = Form(...),
    symptoms: str = Form(...),
    xray_image: UploadFile = File(...)
):
    patient_exists = any(p["id"] == patient_id for p in fake_patients_db)
    if not patient_exists:
        raise HTTPException(status_code=404, detail="존재하지 않는 환자 ID입니다.")

    file_path = MEDIA_DIR / xray_image.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(xray_image.file, buffer)

    record_id = len(fake_records_db) + 1
    new_record = {
        "id": record_id,
        "patient_id": patient_id,
        "chart_number": chart_number,
        "symptoms": symptoms,
        "xray_image_url": f"/media/xrays/{xray_image.filename}"
    }
    fake_records_db.append(new_record)
    return {
        "message": "진료기록과 X-ray 이미지가 성공적으로 등록되었습니다.",
        "data": new_record
    }

@router.get("/records/all", summary="전체 진료기록 목록 조회")
def get_medical_records(patient_id: Optional[int] = None):
    if patient_id:
        return [r for r in fake_records_db if r["patient_id"] == patient_id]
    return fake_records_db