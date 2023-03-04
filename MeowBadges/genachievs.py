from json import load, dump, loads
from scratchattach import Session
from datetime import datetime
from scratchattach import _exceptions as scratch3_errors

def get_stat(stat, username, sess: Session):
    user = sess.connect_user(username)
    if stat == "projects":
        return user.project_count()
    elif stat == "forum_posts":
        return user.forum_counts()['total']['count']
    elif stat == "follow_count":
        return user.follower_count()
    elif stat == "loves_total":
        return user.stats()['loves']
    elif stat == "faves_total":
        return user.stats()['favorites']
    elif stat == "views_total":
        return user.stats()['views']
    else:
        return None

def generate_achievs(user_data: dict, sess):
    try:
        with open("users.json") as cache:
            jsonfile = load(cache)
            if user_data["username"] in jsonfile.keys() or datetime.now().timestamp() - jsonfile['@timestamp'] < 15000:
                print('Used cache data')
                return jsonfile[user_data["username"]]
    except(KeyError):
        pass
    
    achievements = []
    global file
    file = ""
    with open('achievement_list.json') as achlist:
        file = load(achlist)

    for key, value in file.items():
        eligible = False
        if value == "no-requirements":
            eligible = True
        else:
            c = 0
            d = 0
            for req, amt in value.items():
                c += 1
                if get_stat(req, user_data['username'], sess) >= amt:
                    d += 1
            if c == d:
                eligible = True
        if eligible:
            achievements.append(key)
            
    with open("users.json", "r+t") as cache:
        c = loads(cache.read())
        c['@timestamp'] = datetime.timestamp()
        c[user_data["username"]] = achievements
        cache.write("")
        dump(c, cache)
    
    return achievements