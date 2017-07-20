FROM python:3.5

RUN pip install https://github.com/veryhappythings/discord-gather/archive/v0.2.zip

ENV DG_TOKEN your_token_here

CMD discord-gather
