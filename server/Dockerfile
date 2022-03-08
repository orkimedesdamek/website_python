FROM python:alpine
COPY requirements.txt /app
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip cache purge
RUN rm requirements.txt
RUN set -ex && \
    addgroup -S web && \
    adduser -S web -G web
COPY . /app
WORKDIR /app
USER web
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]