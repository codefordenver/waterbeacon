# REF: https://mherman.org/blog/dockerizing-a-react-app/
# BUILD Environment
FROM node:9.6.1 as builder

WORKDIR /app/frontend
COPY . /app/frontend

ENV PATH /app/frontend/node_modules/.bin:$PATH
COPY package.json /app/frontend/package.json

RUN npm install react-scripts@1.1.1 -g --silent
COPY . /app/frontend
RUN npm run build

# #the production environment
FROM nginx:1.13.9-alpine
RUN rm -rf /etc/nginx/conf.d
COPY conf /etc/nginx
COPY --from=builder /app/frontend/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
