FROM python:alpine
RUN set -ex && \
    addgroup -S web && \
    adduser -S web -G web
COPY . /app
WORKDIR /app
USER web
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip cache purge
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]