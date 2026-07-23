# 5일차 - 환자 관리 및 진료기록 API 설계하기

## 1. 개요
- **목적**: 환자 정보 및 진료기록(X-ray 이미지 포함)을 관리하기 위한 REST API 설계
- **프레임워크**: FastAPI, Pydantic

---

## 2. API 엔드포인트 명세

### 📌 [환자 관리 (Patient)]

#### 1. 환자 정보 등록
- **URL**: `POST /patients`
- **설명**: 새로운 환자 정보를 시스템에 등록합니다.
- **Request Body (JSON)**:
  - `name` (string, 필수): 이름
  - `age` (integer, 필수): 나이
  - `gender` (string, 필수): 성별
  - `phone` (string, 필수): 연락처 (휴대폰 번호)
- **Response**: `201 Created`

#### 2. 환자 목록 조회
- **URL**: `GET /patients`
- **설명**: 등록된 환자 목록을 조회합니다. (이름 검색 및 성별/나이 필터링 가능)
- **Query Parameters**:
  - `name` (string, 선택): 이름
  - `gender` (string, 선택): 성별
  - `min_age` / `max_age` (integer, 선택): 나이 범위
- **Response**: `200 OK`

#### 3. 환자 정보 상세 조회
- **URL**: `GET /patients/{patient_id}`
- **설명**: 특정 환자의 상세 정보를 조회합니다.
- **Path Parameter**: `patient_id` (integer)
- **Response**: `200 OK`

#### 4. 환자 정보 수정
- **URL**: `PUT /patients/{patient_id}`
- **설명**: 특정 환자의 정보를 수정합니다.
- **Path Parameter**: `patient_id` (integer)
- **Request Body (JSON)**: `name`, `phone` 등 수정할 정보
- **Response**: `200 OK`

#### 5. 환자 정보 삭제
- **URL**: `DELETE /patients/{patient_id}`
- **설명**: 특정 환자의 정보를 삭제합니다. (연관된 진료기록 및 X-ray 이미지도 함께 삭제)
- **Path Parameter**: `patient_id` (integer)
- **Response**: `200 OK`

---

### 📌 [진료기록 관리 (Medical Record)]

#### 6. 진료기록 등록 (파일 업로드 포함)
- **URL**: `POST /medical-records`
- **설명**: 환자의 진료기록 및 X-ray 이미지를 등록합니다.
- **Request Body (Multipart Form-data)**:
  - `patient_id` (integer, 필수): 환자 ID (교수 ID)
  - `chart_number` (string, 필수): 진료 차트 번호
  - `symptoms` (string, 필수): 진료 증상
  - `xray_image` (File, 필수): X-ray 이미지 파일
- **Response**: `201 Created`

#### 7. 진료기록 목록 조회
- **URL**: `GET /medical-records`
- **설명**: 특정 환자의 진료기록 목록을 조회합니다.
- **Query Parameters**: `patient_id` (integer, 필수)
- **Response**: `200 OK`

#### 8. 진료기록 상세 조회
- **URL**: `GET /medical-records/{record_id}`
- **설명**: 특정 진료기록의 상세 정보 및 X-ray 이미지 정보를 조회합니다.
- **Path Parameter**: `record_id` (integer)
- **Response**: `200 OK`