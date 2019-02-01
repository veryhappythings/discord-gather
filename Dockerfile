FROM python:3.6-alpine3.8

RUN apk update && \
    apk add make git

RUN mkdir /app
WORKDIR /app

COPY test_requirements.txt ./

RUN pip install -r test_requirements.txt
COPY . ./
RUN pip install -e .

CMD discord-gather
