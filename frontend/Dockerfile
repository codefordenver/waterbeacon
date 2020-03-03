# REF: https://mherman.org/blog/dockerizing-a-react-app/
# BUILD Environment
FROM node:8

WORKDIR  /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json

RUN npm install
RUN npm install react-scripts@3.0.1 -g
RUN npm rebuild node-sass

COPY .  /app

EXPOSE 3000
