#!/bin/sh

echo "Starting development env..."

docker-compose up -d

/bin/sh ./open-tty-session.sh
