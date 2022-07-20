FROM python:3

RUN apt update -y

COPY requirements.txt /app/requirements.txt

RUN apt-get install build-essential
RUN pip install -r /app/requirements.txt
RUN pip install debugpy

COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["python3", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]



