#!/bin/bash

# inicjalizuje tabele z modelem fizyczny
psql -f database_init.sql

python ./src/main.py
