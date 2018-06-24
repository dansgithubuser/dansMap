import os
import sys

DIR=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DIR, 'deps'))

import djangogo

parser=djangogo.make_parser()
args=parser.parse_args()
djangogo.main(args,
	project='dansmap',
	app='map',
	database='map_database',
	user='map_database_user',
	heroku_repo='https://git.heroku.com/safe-everglades-62273.git',
	heroku_url='https://safe-everglades-62273.herokuapp.com',
)
