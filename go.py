import argparse
import subprocess
import time

parser=argparse.ArgumentParser()
parser.add_argument('--create-database', '-c', action='store_true')
parser.add_argument('--drop-database', action='store_true')
args=parser.parse_args()

def invoke(*args): subprocess.check_call(args)
def psql(command): invoke('sudo', '-i', '-u', 'postgres', 'psql', '-c', command)

if args.create_database: psql('CREATE DATABASE map_database')

if args.drop_database:
	print('dropping in')
	for i in range(5):
		print(5-i)
		time.sleep(1)
	psql('DROP DATABASE map_database')
