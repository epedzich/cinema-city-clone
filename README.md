# cinema-city-clone
Lighter version of www.cinema-city.pl site based on Cinema City's API

Installation:
------------
1. Setup local environment
2. Clone repo
3. Run ``docker-compose build app``
4. Run ``docker-compose run --rm app python manage.py makemigrations`` and then ``docker-compose run --rm app python manage.py migrate``
5. Run ``docker-compose up --build app``
6. Go to website and enjoy :)
