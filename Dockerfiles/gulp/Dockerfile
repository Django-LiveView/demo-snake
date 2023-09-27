FROM node:18-alpine

WORKDIR /usr/src/app

COPY package.json .
COPY gulpfile.js .

RUN npm install -g npm
RUN npm i --global gulp-cli
RUN npm i
RUN npm cache clean --force

CMD gulp

