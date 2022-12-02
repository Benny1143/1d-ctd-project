from libdw import pyrebase
import colors
from decouple import config

dburl = config('DBURL', default=None)
email = config('EMAIL', default=None)
password = config('PASSWORD', default=None)
apikey = config('APIKEY', default=None)
authdomain = dburl.replace("https://", "") if dburl else None
fallback = True
user = []

if None in [dburl, email, password, apikey]:
    print(colors.Yellow + """Missing .env variables, unable to connect to firebase
Falling back to default values""" + colors.White)
else:
    config = {
        "apiKey": apikey,
        "authDomain": authdomain,
        "databaseURL": dburl,
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    user = auth.refresh(user['refreshToken'])
    fallback = False


def get_highscores() -> dict:
    # Functions return a dict with {name: point} pairs
    if fallback:
        return {"benny": 10, "peter": 3}
    return db.child("highscores").get(user['idToken']).val()
