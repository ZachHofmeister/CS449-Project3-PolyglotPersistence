#!/bin/bash
rm Users.db
sqlite3 Users.db < Users.sql
rm Posts.db
sqlite3 Posts.db < Posts.sql
