FROM python:alpine
RUN addgroup -S web && adduser -S web -G web
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
USER web
HEALTHCHECK NONE
ENTRYPOINT ["python"]
CMD ["server.py"]