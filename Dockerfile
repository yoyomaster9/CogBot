FROM python:3.10

WORKDIR /CogBot

ADD app app

RUN mkdir ./data

RUN pip install discord.py==2.4.0 pyyaml

CMD ["python", "-u", "./app/main.py"]