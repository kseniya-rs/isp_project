FROM nginxinc/nginx-unprivileged:1-alpine


RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

USER root

RUN mkdir -p /vol/web/static
RUN chmod 755 /vol/web/static
