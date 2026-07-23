# [4일차] User API 설계 명세서

## 1. 회원가입 API (REQ-USPR-001)
* **API 이름**: 회원가입 API
* **설명**: 신규 사용자가 시스템에 회원가입을 수행합니다.
* **엔드포인트(Endpoint)**: `/api/v1/users/signup`
* **메서드(Method)**: `POST`
* **인증 필요 여부**: N

### 요청 (Request)
* **Body 필드**:
  * `email` (string, 필수): 사용자 이메일
  * `password` (string, 필수): 비밀번호
  * `name` (string, 필수): 사용자 이름
  * `department` (string, 선택): 부서 (연구, 의료, 개발 등)
  * `gender` (string, 선택): 성별 (M / F)
  * `phone_number` (string, 선택): 휴대폰 번호

### 응답 (Response)
* **201 Created**: 회원가입 성공 및 생성된 사용자 정보 반환

---

## 2. 로그인 API (REQ-USPR-002, 003)
* **API 이름**: 로그인 API
* **설명**: 가입된 사용자가 이메일과 비밀번호로 로그인하여 JWT 토큰을 발급받습니다.
* **엔드포인트(Endpoint)**: `/api/v1/users/login`
* **메서드(Method)**: `POST`
* **인증 필요 여부**: N

### 응답 (Response)
* **200 OK**: 
  * Access Token (Body, 유효기간 30분)
  * Refresh Token (Set-Cookie, HttpOnly, 유효기간 7일)

---

## 3. 회원 정보 조회 API (REQ-USPR-006)
* **API 이름**: 회원 정보 조회 API
* **설명**: 로그인한 사용자가 마이페이지에서 본인의 정보를 조회합니다.
* **엔드포인트(Endpoint)**: `/api/v1/users/me`
* **메서드(Method)**: `GET`
* **인증 필요 여부**: Y

---

## 4. 회원 정보 수정 API (REQ-USPR-007)
* **API 이름**: 회원 정보 수정 API
* **설명**: 로그인한 사용자가 마이페이지에서 본인의 정보(부서, 휴대폰 번호 등)를 수정합니다 (Pydantic 부분 수정 활용).
* **엔드포인트(Endpoint)**: `/api/v1/users/me`
* **메서드(Method)**: `PATCH`
* **인증 필요 여부**: Y

---

## 5. 회원 탈퇴 API (REQ-USPR-009)
* **API 이름**: 회원탈퇴 API
* **설명**: 로그인한 사용자가 마이페이지에서 본인의 계정을 탈퇴합니다.
* **엔드포인트(Endpoint)**: `/api/v1/users/me`
* **메서드(Method)**: `DELETE`
* **인증 필요 여부**: Y