FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pebbleMap ./

EXPOSE 8041
CMD [ "waitress-serve", "--port=8041", '--url-scheme=https', "app:app" ]