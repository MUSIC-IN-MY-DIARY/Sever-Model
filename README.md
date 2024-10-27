# Sever-Model

- 모델서버 
- 개발버전 (Dev 브랜치)
- 모델 테스팅 버전 (model_test 브랜치)

## 현재 구축현황 
1. FastAPI Router 구축 
2. 데이터 매니징 → `data_load.py`
3. 서비스 및 모델 `service` 패키지
4. 도커라이징 진행중 `redis`, `airflow`, `nginx` 완성
5. 아티팩트 레지스트리 세팅 중      

## 트리구조

```bash
.
├── ./LICENSE
├── ./README.md
├── ./Redis
│   ├── ./Redis/Dockerfile
│   └── ./Redis/docker-compose-vectorstore.yaml
├── ./airflow
│   ├── ./airflow/Dockerfile
│   ├── ./airflow/data
│   └── ./airflow/docker-compose-airflow.yaml
├── ./nginx
│   ├── ./nginx/Dockerfile
│   ├── ./nginx/docker-compose-nginx.yaml
│   └── ./nginx/nginx.conf
├── ./service
│   ├── ./service/__pycache__
│   ├── ./service/api
│   ├── ./service/config
│   ├── ./service/main.py
│   ├── ./service/model
│   └── ./service/requirements.txt
└── ./venv
    ├── ./venv/bin
    ├── ./venv/include
    ├── ./venv/lib
    └── ./venv/pyvenv.cfg

```

## 시스템 아키텍처 

![그림](.github/image/Architecture.png)

- 참고사항 
  - `RediSearch` 내에서 벡터 스토어를 사용하기 때문에 `RediSearch`로 사용 
