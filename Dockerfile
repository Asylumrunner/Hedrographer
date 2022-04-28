FROM alpine:3.15.4
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN apk add --no-cache aws-cli

RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --user -r requirements.txt
COPY . . 
ENTRYPOINT ["python3", "bot.py"]