## Kitty names
This repo is where we're going to stash our sources for kitty names, along with any related scripts or code.
## API Endpoints
* /kitty -> [POST and GET] for POST{name: required, description: optional}
* /use_kitty [POST]

### Installation
> Please follow staps below.
1. Create a python3 virtaulenv.
2. Activate the virtualenv.
3. Run `pip install -r requirements.txt` from the home directory of this repo.
4. From the scr directory at the terminal run the command `python app.py`.

### Environment variables
 Thse environment variables are used to determine how the API operates.

1. APP_DATA - Datermines the database to be used. sqlite://kitt_db.sqlite3 is the default.
2. APP_PORT - Determines the port to run on.
3. IS_APP_DATA - when it is not set the app will scrape a site and download certain names to load into database.

