FROM python:slim
COPY . /app
WORKDIR /app
RUN pip install bson
RUN pip install pymongo
RUN pip install flask
ENTRYPOINT ["python"]
CMD ["server.py"]