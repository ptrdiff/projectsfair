#!/bin/sh
wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
heroku container:login
heroku create $HEROKU_APP_NAME
heroku container:push web -a $HEROKU_APP_NAME
heroku container:release web -a $HEROKU_APP_NAME
