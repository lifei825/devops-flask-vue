#!/bin/bash
set -e
# Get the maximum upload file size for Nginx, default to 0: unlimited
USE_NGINX_MAX_UPLOAD=${NGINX_MAX_UPLOAD:-0}
# Generate Nginx config for maximum upload file size
echo "client_max_body_size $USE_NGINX_MAX_UPLOAD;" > /etc/nginx/conf.d/upload.conf


# Generate Nginx config first part using the environment variables
echo 'server {
    location / {
        try_files $uri @app;
    }
    location @app {
        include uwsgi_params;
        uwsgi_pass unix:///tmp/uwsgi.sock;
    }
    '> /etc/nginx/conf.d/nginx.conf

# Finish the Nginx config file
echo "}" >> /etc/nginx/conf.d/nginx.conf

exec "$@"