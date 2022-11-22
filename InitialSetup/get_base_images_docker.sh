docker pull python:3.10-slim-bullseye
docker pull debian:bullseye-slim
docker pull kamailio/kamailio:5.4.6-buster

docker build  -t agiserver:slim-python3.10 --build-arg https_proxy=$http_proxy --build-arg  https_proxy=$http_proxy -f ./Python3/Dockerfile

docker build  -t asterisk:18-slim --build-arg https_proxy=$http_proxy --build-arg  https_proxy=$http_proxy -f ./Asterisk/Dockerfile
