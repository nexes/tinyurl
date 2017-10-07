#!/bin/sh
# waiting for postgresql service

cmd="$@"

# # until psql -h "tinyurldb" -p "5432"  -c "\l"; do
# while ! curl -v -X GET 'tinyurldb:5432/postgres'; do
#     >&2 echo "Connecting to tinyurldb postgres database"
#     sleep 2
# done

# stupid Docker hack, I know.
sleep 5
python manage.py makemigrations --noinput
python manage.py migrate --noinput
exec $cmd