server {
    server_name cargo-logika.ru www.cargo-logika.ru;

    listen 80;
    listen [::]:80;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://cargo-logika.ru$request_uri;
    }
}

server {
    server_name cargo-logika.ru www.cargo-logika.ru;

    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    ssl_certificate /etc/nginx/ssl/live/cargo-logika.ru-0001/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/cargo-logika.ru-0001/privkey.pem;

    client_max_body_size    10M;

    location /static {
        alias /vol/static;
    }

    location / {
    	uwsgi_pass              ${APP_HOST}:${APP_PORT};
        include                 /etc/nginx/uwsgi_params;
    }
}