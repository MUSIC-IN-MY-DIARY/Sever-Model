# 기본 이미지를 Redis Stack으로 설정
FROM redis/redis-stack:latest

COPY .env /etc/environment

ARG REDIS_PASSWORD
ENV REDIS_PASSWORD=$REDIS_PASSWORD