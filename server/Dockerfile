FROM python:alpine
RUN pip install -r requirements.txt
RUN set -ex && \
    addgroup -S web && \
    adduser -S web -G web
COPY . /app
WORKDIR /app
USER web
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]