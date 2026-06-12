#!/usr/bin/env python3
"""Run once on the server to create the admin account: python create_admin.py"""
from mariadb_python import ensure_table, get_user, create_user
from hashing import hash_password

ensure_table()

username = input("Admin username: ").strip()
password = input("Admin password: ").strip()

if not username or not password:
    print("Username and password cannot be empty.")
    raise SystemExit(1)

if get_user(username):
    print(f'User "{username}" already exists.')
    raise SystemExit(1)

create_user(username, hash_password(password), role="admin")
print(f'Admin user "{username}" created.')
