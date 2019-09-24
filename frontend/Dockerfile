# REF: https://mherman.org/blog/dockerizing-a-react-app/
# BUILD Environment
FROM node:9.6.1 as builder
RUN mkdir /app
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app
# COPY package.json yarn.lock public src /app/
# ENV PATH /app/node_modules/.bin:$PATH
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent
RUN npm run build

# #the production environment
# FROM nginx:1.13.9-alpine
# RUN rm -rf /etc/nginx/conf.d
# COPY conf /etc/nginx
# COPY --from=builder /usr/src/app/build /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]


EXPOSE 3000

CMD npm start
