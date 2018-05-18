from collections import defaultdict
import argparse
import os
import subprocess
import sys
import time

parser=argparse.ArgumentParser()
parser.add_argument('--create-database', action='store_true')
parser.add_argument('--drop-database', action='store_true')
parser.add_argument('--create-user', action='store_true')
parser.add_argument('--drop-user', action='store_true', help='as implemented, database must be dropped first')
parser.add_argument('--database-server-start', '--db', action='store_true')
parser.add_argument('--database-server-stop', action='store_true')
parser.add_argument('--deploy-setup', action='store_true')
parser.add_argument('--deploy', '-d', action='store_true')
args=parser.parse_args()

def invoke(*args):
	print('invoking {}'.format(args))
	subprocess.check_call(args)

def postgres(*args): invoke('sudo', '-i', '-u', 'postgres', *args)
def psql(*args): postgres('psql', *args)
def psqlc(command): psql('-c', command)
def psqla(name, value): psqlc("ALTER ROLE map_database_user SET {} TO '{}';".format(name, value))

if args.create_database: psqlc('CREATE DATABASE map_database')

if args.drop_database:
	print('dropping in')
	for i in range(5):
		print(5-i)
		time.sleep(1)
	psqlc('DROP DATABASE map_database')

if args.create_user:
	psqlc("CREATE USER map_database_user WITH PASSWORD 'dev-password';")
	psqla('client_encoding', 'utf8')
	psqla('default_transaction_isolation', 'read committed')
	psqla('timezone', 'UTC')
	psqlc('GRANT ALL PRIVILEGES ON DATABASE map_database TO map_database_user;')

if args.drop_user: psqlc('DROP USER map_database_user')

if args.database_server_start:
	invoke('sudo', 'systemctl', 'start', 'postgresql@10-main')

if args.database_server_stop:
	invoke('sudo', 'systemctl', 'stop', 'postgresql@10-main')

if args.deploy_setup:
	invoke('git', 'remote', 'add', 'heroku', 'https://git.heroku.com/safe-everglades-62273.git')

if args.deploy:
	invoke('git', 'push', 'heroku', 'master')
