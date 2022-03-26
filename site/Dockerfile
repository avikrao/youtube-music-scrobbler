FROM node:10-alpine

WORKDIR /site

EXPOSE 80

RUN npm install express hbs
RUN apk add --update docker openrc
RUN rc-update add docker boot

COPY main.js index.hbs /site/

CMD [ "node", "main.js" ]