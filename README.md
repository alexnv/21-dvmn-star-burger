# Сайт доставки еды Star Burger

Это сайт сети ресторанов Star Burger. Здесь можно заказать превосходные бургеры с доставкой на дом.

![скриншот сайта](https://dvmn.org/filer/canonical/1594651635/686/)


Сеть Star Burger объединяет несколько ресторанов, действующих под единой франшизой. У всех ресторанов одинаковое меню и одинаковые цены. Просто выберите блюдо из меню на сайте и укажите место доставки. Мы сами найдём ближайший к вам ресторан, всё приготовим и привезём.

На сайте есть три независимых интерфейса. Первый — это публичная часть, где можно выбрать блюда из меню, и быстро оформить заказ без регистрации и SMS.

Второй интерфейс предназначен для менеджера. Здесь происходит обработка заказов. Менеджер видит поступившие новые заказы и первым делом созванивается с клиентом, чтобы подтвердить заказ. После оператор выбирает ближайший ресторан и передаёт туда заказ на исполнение. Там всё приготовят и сами доставят еду клиенту.

Третий интерфейс — это админка. Преимущественно им пользуются программисты при разработке сайта. Также сюда заходит менеджер, чтобы обновить меню ресторанов Star Burger.

## Как запустить dev-версию сайта

## Deploy with Docker & HTTPS

[Ссылка на инструкцию.](https://github.com/alexnv/21-dvmn-star-burger/blob/main/DOCKER_DEPLOY_README.md)

## Запуск с Docker

Установите Docker и Docker-compose

[Ссылка на инструкцию.](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/)

Отдельно собирать docker images не надо, их соберет Docker Compose при первом запуске.

Запустите контейнеры:

```shell
docker-compose -f docker-compose.local.yml up
```

Установите nginx
```shell
sudo apt install nginx-full
```

Настройте nginx. Если никогда не работали с ним то вот [ссылка на документацию](https://nginx.org/en/docs/).

Создайте конфиг для nginx. Скопируйте пример конфига ниже, указав свой путь до проекта:
```
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
        alias {your_path_to_star-burger}/media/;
    }

    location /static/ {
        alias {your_path_to_star-burger}/frontend/;
    }

}
```

Скопируйте статику в папку проекта
```shell
docker cp star_burger_web:/code/staticfiles/. ./static/
docker cp star_burger_frontend:/frontend/bundles/. ./static/
```

Проведите миграции:
```shell
docker exec star_burger_web python manage.py migrate --no-input
```

Cоздайте админ пользователя:
```shell
docker exec -it star_burger_web python manage.py createsuperuser
```

Логин от админки - `admin`, пароль - `123456`

Теперь можете зайти на страницу  [http://127.0.0.1/](http://127.0.0.1/).

![](https://i.imgur.com/AOP6G4c.png)

Настройте бэкенд:

Cоздайте файл `.env` в каталоге `star_burger/` со следующими настройками:

Все настройки, кроме отмеченных звёздочкой `*` необязательные. Для local окружения можно не настраивать.

- `ROLLBAR_ENVIRONMENT_NAME` — в Rollbar задаёт название окружения или инсталляции сайта;
- `ROLLBAR_ACCESS_TOKEN` — API ключ от [rollbar](https://rollbar.com/), находится в ваших проектах;
- *`POSTGRES_USER` — Логин от postgres user'а;
- *`POSTGRES_PASSWORD` — Пароль от postgres user'а;
- `POSTGRES_HOST` — Адрес от postgres;
- `POSTGRES_PORT` — Порт от postgres;
- `DEBUG` — Дебаг-режим; Поставьте `False`;
- `YANDEX_API_KEY` — API ключ от яндекс гео-кодера;
- *`SECRET_KEY` — Секретный ключ проекта. Он отвечает за шифрование на сайте/ Например, им зашифрованы все пароли на вашем сайте;
- `ALLOWED_HOSTS` — [см; документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).

## Координаты сервера

Домен: [85.193.80.53.nip.io](https://85.193.80.53.nip.io/)


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org). За основу был взят код проекта [FoodCart](https://github.com/Saibharath79/FoodCart).

Где используется репозиторий:

- Второй и третий урок [учебного курса Django](https://dvmn.org/modules/django/)
