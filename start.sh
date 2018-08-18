python3 manage.py runserver $(/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1):8000
