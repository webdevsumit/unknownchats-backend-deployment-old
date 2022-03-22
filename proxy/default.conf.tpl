
server {
    listen ${LISTEN_PORT};

    location /static {
        alias /vol/static;
    }

    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    300M;
    }
}

server {
    listen 443 ssl;
    ssl on;

    server_name  backend.unknownchats.com;
    ssl_certificate /etc/nginx/certs/certificate.crt;
    ssl_bundle /etc/nginx/certs/ca_bundle.crt;
    ssl_certificate_key /etc/nginx/certs/private.key;

    location /static {
        alias /vol/static;
    }
    
    location / {
        uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
        client_max_body_size    300M;
    }
}