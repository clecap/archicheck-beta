FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/bin/src/webapp/src
RUN apt update && apt upgrade -y
RUN apt install gpg -y
RUN python -m pip install --upgrade pip
RUN pip install pymongo==3.12
RUN pip install pycryptodome

