#!/bin/bash
rm Posts.db
sqlite3 Posts.db < Posts.sql
