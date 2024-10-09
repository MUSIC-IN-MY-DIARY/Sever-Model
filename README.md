# Sever-Model

- 모델서버 

## 현재 구축현황 
1. FastAPI Router 구축 
2. 데이터 매니징 → `data_load.py`
3. 서비스 및 모델 `service` 패키지

## 트리구조

```bash
.
├── LICENSE
├── README.md
├── data
│   ├── data_load.py
│   ├── redis_data
│   └── test_data.json
├── service
│   ├── __pycache__
│   ├── api
│   ├── config
│   ├── main.py
│   ├── model
│   └── requirments.txt
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg

```

## 시스템 아키텍처 

![그림](.github/image/Architecture.png)

- 참고사항 
  - `RediSearch` 내에서 벡터 스토어를 사용하기 때문에 `RediSearch`로 사용 
