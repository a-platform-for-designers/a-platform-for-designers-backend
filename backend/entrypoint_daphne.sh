#!/bin/bash

./wait-for-it.sh db:5432 --timeout=30

exec daphne -b 0.0.0.0 -p 8001 designers.asgi:application
