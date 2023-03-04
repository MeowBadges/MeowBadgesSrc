from flask import Flask, request, render_template
import requests
import json
import scratchattach as scratch3
from scratchattach import _exceptions as scratch3_errors
from genachievs import generate_achievs
from urllib.parse import quote as encode_url_component

def get_session_token():
    with open('.env', 'rt') as file:
        return json.load(file)['sessionToken']

session = scratch3.Session(get_session_token(), username="Redstone1080")

app = Flask(__name__)

LINKS = ['home', 'search']

def parse_requirements(requirements):
    return ""

def get_ocular_status(uname):
    r = requests.get(f'https://my-ocular.jeffalo.net/api/user/{uname}')
    j = json.loads(r.text)
    if 'error' in j.keys():
        return None
    else:
        return j['status']
    
def get_pfp_src(uname):
    r = requests.get(f'https://api.scratch.mit.edu/users/{uname}')
    j = json.loads(r.text)
    
    pfp_url = j['profile']['images']['90x90']
    return f'https://corsproxy.io/?{encode_url_component(pfp_url)}'

@app.get('/')
def index():
    return app.redirect('/home')

@app.get('/home')
def home():
    return render_template('index.html', links=LINKS)

@app.get('/users')
def users():
    
    dict_ = {}
    
    global sessu
    try:
        sessu = session.connect_user(request.args.get('user'))
    except scratch3_errors.UserNotFound:
        return render_template('user-not-found.html', links=LINKS), 404
    
    dict_['username'] = sessu.username
    dict_['ocular'] = get_ocular_status(dict_['username'])
    dict_['bio'] = "ǮǮ".join(sessu.about_me.split('\n'))
    dict_['wiwo'] = "ǮǮ".join(sessu.wiwo.split('\n'))
    try:
        dict_['achievements'] = generate_achievs(dict_, session)
    except(scratch3_errors.FetchError):
        dict_['achievements'] = ['error']
    dict_['pfp_src'] = get_pfp_src(dict_['username'])
    dict_['achiev_requirements'] = json.loads(open('achievement_list.json', 'rt').read())
    
    return render_template('users.html', links=LINKS, q=dict_, parse_requirements=parse_requirements)

@app.get('/search')
def search():
    return render_template('search.html', links=LINKS)

@app.get('/attrib')
def attrib():
    return render_template('attribution.html', links=LINKS)

app.run(host='localhost', port=3000, debug=True)
