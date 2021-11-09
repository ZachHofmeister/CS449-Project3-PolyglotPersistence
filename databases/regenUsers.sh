#!/bin/bash
rm Users.db
sqlite3 Users.db < Users.sql
