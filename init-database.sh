#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE ROLE article WITH LOGIN PASSWORD 'F23jfyq$341asDF';
    CREATE DATABASE article_django;
    GRANT ALL PRIVILEGES ON DATABASE article_django TO article;
EOSQL
