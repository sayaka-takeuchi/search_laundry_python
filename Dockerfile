FROM python:3

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update
RUN apt-get -y install vim
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 8001

CMD ["python", "run.py"]