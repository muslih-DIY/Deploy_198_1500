podman pull python:3.10-slim-bullseye
podman pull debian:bullseye-slim
podman pull kamailio/kamailio:5.4.6-buster


buildah build-using-dockerfile  -t agiserver:slim-python3.10 --build-arg https_proxy=http://xx.xx.xx.xx:3128 --build-arg  https_proxy=http://xx.xx.xx.xx:3128  .

buildah build-using-dockerfile  -t asterisk:18-slim --build-arg https_proxy=http://xx.xx.xx.xx:3128 --build-arg  https_proxy=http://xx.xx.xx.xx:3128 .
