FROM jwilder/nginx-proxy

RUN rm /etc/nginx/conf.d/default.conf
COPY /nginx/vhost.d/default /etc/nginx/vhost.d/default
COPY custom.conf /etc/nginx/conf.d/custom.conf
