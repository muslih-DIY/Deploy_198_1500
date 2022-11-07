FROM python:3.10-slim-bullseye AS stage

WORKDIR /apps
RUN apt-get update && apt-get -y --no-install-recommends \
    install libpq-dev \
    procps \
    gcc \
    python3-dev 

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim-bullseye AS run-time
RUN apt-get update && apt-get -y --no-install-recommends \
    install libpq-dev procps \
    && apt-get purge -y --auto-remove \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
ENV VIRTUAL_ENV=/apps/venv
COPY --from=stage /opt/venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH="/apps/:$PYTHONPATH"
WORKDIR /apps
COPY entrypoint.sh .
COPY ./AGISERVER/ ./
CMD [ "bash","./entrypoint.sh" ]
# CMD ["python3", "/apps/Agiserver/core/main.py", "host=0.0.0.0"]
# python3 /apps/Agiserver/core/main.py host=0.0.0.0