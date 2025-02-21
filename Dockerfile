FROM  python:3.12.3

RUN mkdir -p /usr/www/logs
RUN mkdir -p /usr/www/media

RUN python -m pip install --upgrade pip

WORKDIR /usr/www/

COPY . .

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y gettext

# EXPOSE 8000

# Start the app using serve command
# CMD [  ]