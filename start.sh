#!/bin/bash

export $(grep -v '^#' .env | xargs)

fuser -k $PORT/tcp

cd $WORK_DIR

exec nohup uwsgi -w index:app --logto $WORK_DIR/index.log --http $HOST:$PORT --ini index.ini > index.error &