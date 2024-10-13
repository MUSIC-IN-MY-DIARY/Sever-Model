FROM redis/redis-stack:latest

# 환경변수

ARG REDIS_PASSWORD
ENV REDIS_PASSWORD=$REDIS_PASSWORD

COPY .env /etc/environment

# redis-server를 비밀번호로 실행하도록 설정
CMD ["redis-server", "--requirepass", "$REDIS_PASSWORD"]