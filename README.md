## Stitch It API
[Stitch It](https://github.com/krnorris65/stitch-it-app) is a front-end React app that allows stitchers to keep track of their own cross stitch projects as well as follow other stitchers and see their cross stitch projects. 

Stitch It API is a Django REST API that Stitch It connects to in order to store data.

### Initial setup to run this app:
1) Clone repo:
`git clone git@github.com:krnorris65/stitch-it-api.git`

1) After repo is cloned, navigate to the root directory:
`cd stitch-it-api`

1) Create virtual environment: 
`python -m venv StitchItEnv`

1) Activate the virtual environment: 
`source ./StitchItEnv/bin/activate`

1) Install dependencies for the app: 
`pip install -r requirements.txt`

1) Run migrations to create the database:
`python manage.py migrate`

1) Pre-populate the Fabrics table with some data from fixtures:
`python manage.py loaddata fabrics`

1) Pre-populate the Sizes table with some data from fixtures:
`python manage.py loaddata sizes`

1) Run this app:
`python manage.py runserver`

1) Clone and run front-end application, [Stitch It](https://github.com/krnorris65/stitch-it-app), for complete full stack app.

Optional:
1) After creating at least 2 stitchers, you can populate the Designs table with some data from fixtures for stitchers with ids 1 & 2:
`python manage.py loaddata designs`
1) After creating at least 4 stitchers, you can populate the Follows table with some data from fixtures:
`python manage.py loaddata follows`

### Run this app after initial setup:
1) Navigate to root directory of this app
1) Activate the virtual environment: 
`source ./StitchItEnv/bin/activate`
1) Run the app:
`python manage.py runserver`