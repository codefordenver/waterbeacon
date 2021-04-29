# REF: https://mherman.org/blog/dockerizing-a-react-app/
# BUILD Environment
FROM node:14

WORKDIR  /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json

RUN npm install

COPY .  ./

CMD ["npm", "start"]
