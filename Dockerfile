#FROM nikolaik/python-nodejs:python3.9-nodejs16-alpine
FROM alpine:3.15.4
RUN apk add --no-cache npm
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN npm install pm2@latest -g
RUN apk add --no-cache aws-cli

RUN addgroup app && adduser -S -G app app
USER app
WORKDIR /app
COPY . . 
RUN pip3 install --user -r requirements.txt
ENTRYPOINT ["pm2", "start", "bot.py", "--name", "Hedrographer", "--interpreter", "python3"]