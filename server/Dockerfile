FROM python:alpine
RUN set -ex && \
    addgroup -S web && \
    adduser -S web -G web
COPY . /app
WORKDIR /app
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
USER web
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]