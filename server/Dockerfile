FROM python:alpine
RUN set -ex && \
    addgroup -S web && \
    adduser -S web -G web
WORKDIR /app
USER web
COPY requirements.txt /app
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip cache purge
COPY . /app
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]