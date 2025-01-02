# 베이스 이미지 선택
FROM python:3.10-slim

# 1. 기본 디렉토리 설정
WORKDIR /app

# 2. 필요한 파일 복사
# requirements.txt 복사 후 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 프로젝트 전체 복사
COPY . /app

# # 3. 환경 변수 설정 (필요시 추가)
# ENV PYTHONUNBUFFERED=1

# 4. 기본 실행 명령 설정
CMD ["python", "service/main.py"]