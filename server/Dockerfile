FROM python:alpine
RUN useradd -r -g web web
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
USER web
ENTRYPOINT ["python"]
CMD ["server.py"]