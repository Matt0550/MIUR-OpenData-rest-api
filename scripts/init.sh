#!/bin/bash

# Get PORT and HOST from environment variables
PORT=5000
HOST="0.0.0.0"

if [ ! -z "$PUID" ] && [ ! -z "$PGID" ]; then
    groupmod -g $PGID $APP_USER
    usermod -u $PUID -g $PGID $APP_USER

    chown -R $PUID:$PGID /home/app
    # Workdir
    cd /home/app

    exec gosu $APP_USER uvicorn main:app --port $PORT --host $HOST
else
    chown -R 0:0 /home/app
    
    # Workdir
    cd /home/app

    exec uvicorn main:app --port $PORT --host $HOST
fi