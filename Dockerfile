FROM python:3.6

RUN pip install https://github.com/veryhappythings/discord-gather/archive/v0.4.zip

ENV DG_TOKEN your_token_here

CMD discord-gather
