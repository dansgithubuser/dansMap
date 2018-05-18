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
parser.add_argument('--drop-user', action='store_true')
args=parser.parse_args()

def invoke(*args): subprocess.check_call(args)
def psql(*args): invoke('sudo', '-i', '-u', 'postgres', 'psql', *args)
def psqlc(command): psql('-c', command)

if args.create_database: psqlc('CREATE DATABASE map_database')

if args.drop_database:
	print('dropping in')
	for i in range(5):
		print(5-i)
		time.sleep(1)
	psqlc('DROP DATABASE map_database')

if args.create_user:
	sys.path.append(os.path.join('dansmap'))
	import settings_secret
	recursive_defaultdict_builder=lambda: defaultdict(recursive_defaultdict_builder)
	configuration=recursive_defaultdict_builder()
	settings_secret.inject(configuration)
	psqlc("CREATE USER map_database_user WITH PASSWORD '{}';".format(configuration['DATABASES']['default']['PASSWORD']))

if args.drop_user: psqlc('DROP USER map_database_user')
