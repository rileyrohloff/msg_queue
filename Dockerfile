FROM alpine:3.9

LABEL maintainer="Riley Rohloff <ryatthegym@gmail.com>"

RUN apk upgrade && \
    apk add bash gcc libc-dev python3-dev libffi-dev openssl-dev nodejs npm

COPY . /app
WORKDIR /app
# setups environment for proxy
RUN pip3 install -r reqs.txt
RUN pip3 install --upgrade pip setuptools

EXPOSE 5000
CMD ["python3","manage.py", "runserver", "0.0.0.0:5000"]
