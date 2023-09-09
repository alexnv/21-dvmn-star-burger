# Инструкция по деплою на сервер

## Процесс деплоя (Linux)

Купите домен и отправляйте все запросы ip вашего сервера

Настройте .env файл:

> [ссылка на инструкцию](https://github.com/depocoder/star-burger/blob/main/README.md#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D1%82%D0%B5-%D0%B1%D1%8D%D0%BA%D0%B5%D0%BD%D0%B4)

Создайте external docker network

```shell
docker network create db_network
```

Запустите контейнеры

```shell
docker-compose -f docker-compose.production.web.yml -f docker-compose.production.db.yml up -d
```

Настройте nginx. Если никогда не работали с ним то вот [ссылка на документацию](https://nginx.org/en/docs/).

Создайте конфиг для nginx. Скопируйте пример конфига ниже, указав свой путь до проекта:

```nginx
server {
    listen 80 default;

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8080/;
    }

    location /media/ {
        alias {your_path_to_media}/media/;
    }

    location /static/ {
        alias {your_path_to_frontend}/frontend/;
    }

}
```

Создайте сертификаты. Для этого рекомендую использовать [certbot](https://certbot.eff.org/).

Теперь можете зайти адрес по домену на сервер у меня это  [https://starburger.depocoder.xyz/](https://starburger.depocoder.xyz/).

![](https://i.imgur.com/6eIGuKj.png)


Проведите миграции
```shell
docker exec star_burger_web python manage.py migrate --no-input
```

Соберите статику
```shell
docker cp star_burger_web:/code/staticfiles/. ./static/
docker cp star_burger_frontend:/frontend/bundles/. ./static/
```

## Автообновление сертификатов Certbot
Сертификаты от certbot действительны 3 месяца, поэтому их надо иногда обновлять.

Рекомендую для обновления воспользовать [systemd](https://en.wikipedia.org/wiki/Systemd) для создания сервиса по автообновления сертификата.

Если с systemd вы не работали, то рекомендую обратиться к статье [Systemd за пять минут](https://habr.com/ru/company/southbridge/blog/255845/)

Пример сервиса по запуску
```
# Содержимое файла /etc/systemd/system/certbot-renewal.service
[Unit]
Description=Certbot Renewal

[Service]
ExecStart=/usr/bin/certbot renew --force-renewal --post-hook "systemctl reload nginx.service"
```

Пример таймера
```
# Содержимое файла /etc/systemd/system/certbot-renewal.timer
[Unit]
Description=Timer for Certbot Renewal

[Timer]
OnBootSec=300
OnUnitActiveSec=1w

[Install]
WantedBy=multi-user.target
```

## Автоочистка django sessions

Рекомендую воспользоваться systemd.

Пример сервиса:
```
# Содержимое файла /etc/systemd/system/starburger-clearsessions.service
[Service]
WorkingDirectory="CHANGE ME TO YOUR PATH"
ExecStart=docker exec star_burger_web "python" "manage.py" "clearsessions"

[Install]
WantedBy=multi-user.target
```

Пример таймера:
```
# Содержимое файла /etc/systemd/system/starburger-clearsessions.timer
[Unit]
Description=Timer for clear star burger sessions

[Timer]
OnBootSec=300
OnUnitActiveSec=1w

[Install]
WantedBy=multi-user.target
```

## Как быстро обновить код на развернутом сервере?
В репозитории есть заготовка для быстрого обновления кода.
```shell
./deploy_star_burger.sh
```

## Запуск тестов
```shell
docker exec star_burger_web python manage.py test
```



