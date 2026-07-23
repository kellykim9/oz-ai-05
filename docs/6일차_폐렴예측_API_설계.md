# 6일차 - AI 폐렴 예측 API 설계서

## 1. 개요
사내 의료인, 개발실, 연구자 권한을 가진 유저가 진료 기록을 바탕으로 AI 폐렴 예측 모델을 실행하고 결과를 조회할 수 있는 API 명세서입니다.

---

## 2. API 엔드포인트 명세

### (1) AI 모델 활용 폐렴 예측 수행
* **요구사항 ID**: REQ-PRED-001
* **URL**: `POST /api/medical-records/{record_id}/predict-pneumonia`
* **설명**: 진료 기록에 업로드된 X-ray 이미지를 바탕으로 AI 폐렴 예측을 수행합니다. 이미 예측된 결과가 있다면 추론 과정을 거치지 않고 저장된 데이터를 응답합니다.
* **Request (요청 데이터)**:
  * Headers: `Authorization: Bearer <Token>` (의료인/개발자/연구자 권한 필요)
  * Path Parameter: `record_id` (진료 기록 고유 ID)
* **Response (응답 데이터)**:
  ```json
  {
    "success": true,
    "data": {
      "is_pneumonia": true,
      "confidence": 0.95,
      "heatmap_image_url": "[https://example.com/images/heatmap_123.png](https://example.com/images/heatmap_123.png)"
    }
  }