FROM python:3.8-slim
WORKDIR /api
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY app/ ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
