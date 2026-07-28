# 🫁 폐렴 환자 관리 백오피스 프로젝트

의료 이미지(X-ray) 기반 폐렴 분류 AI 모델을 내부 관리용 백오피스와 연동한 개인 프로젝트입니다.

## 주요 기능
- X-ray 이미지 업로드
- AI 예측 결과 확인
- 환자 정보 조회 및 관리
- FastAPI 기반 API 연동
- Docker 환경에서 실행 및 배포

## 기술 스택
Python · FastAPI · PyTorch · Redis · MySQL · Docker · AWS

---
## 🚀 프로젝트 과정 총 정리

1. **Team Rule 정의**: 그라운드 루루 및 협업 규칙 설정
2. **사용자 요구사항 정의**: 서비스에 필요한 기능 및 요구사항 분석
3. **API 명세서 작성**: 클라이언트와 서버 간의 API 규격 정의
4. **Git & Github Branch 전략 구성**: Git 브랜치 전략(main, develop, feature 등) 수립
5. **프로젝트 세팅**: FastAPI 및 기본 개발 환경 구성
6. **API 및 AI 워커 코드 작성 후 Branch 전략을 통한 코드 병합**: 기능별 브랜치 생성 및 PR/Merge 수행
7. **아키텍처 설계 및 적용**: Redis와 FastAPI를 활용한 Event-Driven Architecture 설계
8. **도커 인프라 관련 파일 작성**: Dockerfile 및 Docker Compose를 통한 MySQL, Redis 컨테이너 구축
9. **AWS 배포**: 클라우드 서버에 서비스 배포
10. **QA 진행**: 테스트 및 오류 수정
