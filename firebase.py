from libdw import pyrebase
import colors
from decouple import config

dburl = config('DBURL', default=None)
email = config('EMAIL', default=None)
password = config('PASSWORD', default=None)
apikey = config('APIKEY', default=None)
authdomain = dburl.replace("https://", "") if dburl else None
fallback = True

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
    fallback = False


def get_highscores() -> dict[str, int]:
    # Functions return a dict with {name: point} pairs
    if fallback:
        return {"benny": 10, "peter": 3}
    return db.child("highscores").get().val()


def get_user_scores(name) -> dict[int, int]:
    # Functions return a dict with {map: point} pairs
    # Returns None if name or map is not found
    if fallback:
        return {1: 4, 2: 6}
    info = db.child("users").child(name).child("map").get()
    dic = {user.key(): user.val() for user in info.each()}
    if 0 in dic:
        del dic[0]
    return dic


def get_user_scores_by_map(name, map) -> int:
    # Functions return the points for the specific map
    # Returns None if name or map is not found
    if fallback:
        return get_user_scores(name)[map]
    return db.child("users").child(name).child("map").child(map).get().val()


def get_user_map_scores(name):
    return db.child("users").child(name).child("map").get()


def update_user_scores_by_map(name, map, score):
    # name (str), map (str), score (int)
    db.child("users").child(name).child("map").child(map).set(score)

#update_user_scores_by_map("peter", "1", 4)


def update_user_scores(name):
    # name (str)
    total = 0
    for i in get_user_map_scores(name).val():
        if i != None:
            total += i
    db.child("highscores").child(name).set(total)


# update_user_scores("a")
