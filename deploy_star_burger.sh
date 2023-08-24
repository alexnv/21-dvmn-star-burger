cd /opt/21-dvmn-star-burger/
echo "******************Обновляем код репозитория******************"
git pull
echo
echo
echo "******************Устанавливаем бибилиотеки Python******************"
source .venv/bin/activate
pip install -r requirements.txt
echo
echo
echo "******************Устанавливаем бибилиотеки Node.js******************"
npm install --dev
echo
echo
echo "******************Сборка фронтенда******************"
parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo
echo
echo "******************Сборка статики Django******************"
python manage.py collectstatic --noinput
echo
echo
echo "******************Применение миграций Django******************"
python manage.py migrate --noinput
echo
echo
echo "******************Перезапуск сервисов Systemd******************"
systemctl reload nginx.service
systemctl restart 21-dvmn-star-burger