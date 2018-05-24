from collections import defaultdict
import argparse
import os
import subprocess
import sys
import time
import webbrowser

parser=argparse.ArgumentParser()
parser.add_argument('--create-database', action='store_true')
parser.add_argument('--drop-database', action='store_true')
parser.add_argument('--create-user', action='store_true')
parser.add_argument('--drop-user', action='store_true', help='as implemented, database must be dropped first')
parser.add_argument('--database-freshen', action='store_true', help='drop database and user; create database and user')
parser.add_argument('--database-server-start', '--db', action='store_true')
parser.add_argument('--database-server-stop', action='store_true')
parser.add_argument('--migrate', action='store_true')
parser.add_argument('--deploy-setup', action='store_true')
parser.add_argument('--deploy', '-d', action='store_true')
parser.add_argument('--log', '-l', action='store_true')
parser.add_argument('--run', '-r', action='store_true')
parser.add_argument('--heroku-psql', action='store_true')
parser.add_argument('--browser', '-b', action='store_true')
args=parser.parse_args()

def invoke(*args):
	print('invoking {}'.format(args))
	subprocess.check_call(args)

def postgres(*args): invoke('sudo', '-i', '-u', 'postgres', *args)
def psql(*args): postgres('psql', *args)
def psqlc(command): psql('-c', command)
def psqla(name, value): psqlc("ALTER ROLE map_database_user SET {} TO '{}';".format(name, value))

def create_database(): psqlc('CREATE DATABASE map_database')
if args.create_database: create_database()

def drop_database(): psqlc('DROP DATABASE map_database')
if args.drop_database: drop_database()

def create_user():
	psqlc("CREATE USER map_database_user WITH PASSWORD 'dev-password';")
	psqla('client_encoding', 'utf8')
	psqla('default_transaction_isolation', 'read committed')
	psqla('timezone', 'UTC')
	psqlc('GRANT ALL PRIVILEGES ON DATABASE map_database TO map_database_user;')
if args.create_user: create_user()

def drop_user(): psqlc('DROP USER map_database_user')
if args.drop_user: drop_user()

if args.database_freshen:
	drop_database()
	drop_user()
	create_database()
	create_user()

if args.database_server_start:
	invoke('sudo', 'systemctl', 'start', 'postgresql@10-main')

if args.database_server_stop:
	invoke('sudo', 'systemctl', 'stop', 'postgresql@10-main')

if args.migrate:
	invoke('python3', 'manage.py', 'makemigrations', 'map')
	invoke('python3', 'manage.py', 'migrate')

if args.deploy_setup:
	invoke('git', 'remote', 'add', 'heroku', 'https://git.heroku.com/safe-everglades-62273.git')

if args.deploy:
	invoke('python3', 'manage.py', 'check', '--deploy')
	invoke('heroku', 'run', 'python', 'manage.py', 'migrate')
	invoke('git', 'push', '-f', 'heroku', 'master')

if args.log:
	invoke('heroku', 'logs', '--tail')

if args.run:
	invoke('python3', 'manage.py', 'runserver', '--settings', 'dansmap.settings_debug')

if args.heroku_psql:
	invoke('heroku', 'pg:psql')

if args.browser:
	webbrowser.open_new_tab('https://safe-everglades-62273.herokuapp.com')
