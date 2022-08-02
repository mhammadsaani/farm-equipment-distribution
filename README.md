# Farm Equipment Distribution

Final year project

### Requirements

-   Python 3
-   Git
-   Database: Sqlite, Mysql, Postgres

### Installation

-   `git clone https://github.com/6hislain/farm-equipment-distribution`
-   `cd farm-equipment-distribution`
-   `python3 -m venv venv`
-   `source venv/bin/activate`
-   `pip install -r requirements.txt`
-   edit `mysite/settings.py` to match your preference
-   `python3 manage.py migrate`
-   `python3 manage.py createsuperuser`
-   `python3 manage.py runserver`

### Todo

-   [ ] form validation
-   [x] search
-   [x] pagination
-   [x] return JSON from model
-   [x] redirect from urls.py

App Models

-   [x] after sale service: product, partner, service, tag
-   [x] chat: message
-   [x] main: user profile, notification, settings, search history
-   [x] qna: question, answer
-   [x] timeline: article, post
