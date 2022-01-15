FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pebbleMap ./
COPY entrypoint.sh ./

EXPOSE 8041
ENTRYPOINT ["./entrypoint.sh"]