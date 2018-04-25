## Kitty names
This repo is where we're going to stash our sources for kitty names, along with any related scripts or code.
## API Endpoints
* /kitty -> Accepts [POST and GET]. For POST send JSON object with {name: <type: string, required: true>, description: <type: string, optional: true>} and for GET a JSON object {description: <type: string>, id: <type: int>, name: <type: string>} if name is found or {message: <type: string>} otherwise, is returned. POST returns 201 on success and 400 on bad request. GET return 200 if a name is found and 404 otherwise.
* /use_kitty/<int: id> -> Accepts [PATCH and PUT]. Changes kitty->used to true, for the kitty->id. Returns 200 on success, 404 if kitty with id was not found and 406 if kitty->id had already been used.

### Installation
> Please follow staps below.
1. Create a python3 virtaulenv.
2. Activate the virtualenv.
3. Run `pip install -r requirements.txt` from the home directory of this repo.
4. From the scr directory at the terminal run the command `python app.py`.

> Note: the installation steps above are for working in a development environment.
> for production environment please use WSGI with a production grade server.

### Environment variables
 These environment variables are used to determine how the API operates.

1. APP_PORT - Determines the port to run on. Defaults to port 3000.
2. DATABASE_URL - Datermines the database to be used. Dafaults to sqlite:///kitt_db.sqlite3.
3. HOST - This environment variable is used to determine whether to run locally or open to outside requests. Defaults to ouside request.
Set to `localhost` host if you only want listen locally.
4. IS_APP_DATA - When it is not set the app will scrape a site and download certain names to load into database.
You can set this to any garbage value, and the app will avoid scraping the site. Otherwise, the app will scrape the site.

# TODO
Load other data to the database.
```
    KittyName(name=name, description=dercription, used=False)
    db.session.add(kitty)
    db.session.commit()
```
Loads a kitty name into the database.
Refer to `load_data()` function in src/app.py for an example of how this is done.
