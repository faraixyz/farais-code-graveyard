from base64 import urlsafe_b64encode
from hashlib import sha1
import hmac
import json
import pprint
import secrets
from urllib.parse import quote_plus, quote
from time import time
import requests

with open('config.json', 'rb') as config_file:
	CONFIG = json.load(config_file)

#Defaults
oauth_consumer_key = CONFIG['consumer']['key']
oauth_signature_method = "HMAC-SHA1"
oauth_token = CONFIG['user']['key']
oauth_version = '1.0'
SIGN_KEY = bytes(CONFIG['consumer']['secret']+'&'+CONFIG['user']['secret'], 'utf-8')

def signrequest(request):
	signer = hmac.new(SIGN_KEY, bytes(request,'utf-8'), sha1)
	digest = urlsafe_b64encode(signer.digest())
	
	return digest.decode('utf-8')
	
def make_oauth_obj():
	oauth_nonce = secrets.token_urlsafe(16)
	oauth_timestamp = time()
	return {
		"oauth_consumer_key":oauth_consumer_key,
		"oauth_nonce":oauth_nonce,
		"oauth_signature_method":oauth_signature_method,
		"oauth_timestamp":oauth_timestamp,
		"oauth_token":oauth_token,
		"oauth_version":oauth_version,
	}

def make_sign_str(method, url, oauth_obj, params):
	sign_str = f"{method}&{quote_plus(url)}&"
	for key, val in sorted([*oauth_obj.items(), *params.items()]):
		sign_str += f"{quote_plus(key)}%3D{quote_plus(str(val))}%26"
	
	return sign_str[:-3]

def make_auth_header(oauth_obj):
	header = "OAUTH "
	oauth_prop = [f'{quote_plus(key)}="{quote_plus(str(value))}"' for key, value in sorted(oauth_obj.items())]
	header += ", ".join(oauth_prop)
	return header

def get_friends():
	url = 'https://api.twitter.com/1.1/friends/ids.json'
	method = "GET"
	oauth = make_oauth_obj()
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.get(url, headers=headers)
	
	ids = r.json()['ids']
	return ids

def get_friends_with_hidden_retweets():
	url = 'https://api.twitter.com/1.1/friendships/no_retweets/ids.json'
	method = "GET"
	oauth = make_oauth_obj()
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.get(url, headers=headers)
	
	ids = r.json()
	return ids

def hide_retweets_from_user(id):
	url = "https://api.twitter.com/1.1/friendships/update.json"
	method = "POST"
	oauth = make_oauth_obj()
	args = {"user_id":id, "retweets":False}
	sign_string = make_sign_str(method, url, oauth, args)
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.post(url, data=args, headers=headers)
	
	return r

def get_tweets():
	url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
	method = 'GET'
	oauth = make_oauth_obj()
	args = {"trim_user": 1}
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.get(url, headers=headers)
	data = r.json()
	ids = list(map(lambda x: x['id_str'], data))

	return ids

def get_favorites():
	url = 'https://api.twitter.com/1.1/favorites/list.json'
	method = 'GET'
	oauth = make_oauth_obj()
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.get(url, headers=headers)
	data = r.json()
	ids = list(map(lambda x: x['id_str'], data))

	return ids
	
def delete_tweet(id):
	url = f'https://api.twitter.com/1.1/statuses/destroy/{id}.json'
	method = 'POST'
	oauth = make_oauth_obj()
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.post(url, data={}, headers=headers)

def make_fav(id):
	url = 'https://api.twitter.com/1.1/favorites/create.json'
	method = 'POST'
	oauth = make_oauth_obj()
	args = {'id':id}
	sign_string = make_sign_str(method, url, oauth, args)
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.post(url, data=args, headers=headers)

def delete_fav(id):
	url = 'https://api.twitter.com/1.1/favorites/destroy.json'
	method = 'POST'
	oauth = make_oauth_obj()
	args = {'id':id}
	sign_string = make_sign_str(method, url, oauth, args)
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.post(url, data=args, headers=headers)
	
def rate_limit():
	url = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
	method= 'GET'
	oauth = make_oauth_obj()
	sign_string = make_sign_str(method, url, oauth, {})
	oauth["oauth_signature"] = signrequest(sign_string)
	headers = {"Authorization":make_auth_header(oauth)}
	r = requests.get(url, headers=headers)
	return r.json()

def delete_tweets():
	deleted = 0
	while True:
		a = get_tweets()
		print(a)
		for i in a:
			delete_tweet(i)
			print('Deleted ' + i)
			deleted +=1
		print(f'{deleted} tweets deleted so far')

def hide_retweets_from_friends():
	friends = get_friends()
	unretweeted = get_friends_with_hidden_retweets()
	retweeded = list(filter(lambda x:x not in unretweeted, friends))
	log = []
	print(retweeded)
	try:
		for user in retweeded:
			out = hide_retweets_from_user(user)
			log.append(out)
	except Exception as e:
		print("Something went Wrong")
		raise(e)

	print("All done!")
	
def delete_favs():
	for i in range(200):
		a = get_favorites()
		print(a)
		for i in a:
			make_fav(i)
			print(f'liked {i}')
			delete_fav(i)
			print(f'deleted {i}')
		print('eh')
	
'''
# The following code was a more complex means of deleting favs
# Takes forever and Twitter doesn't like it.

with open('like','r') as likes:
	likes = likes.read().splitlines()

try:
	deleted = 0
	while True:
		tweet = likes.pop()
		print(tweet)
		make_favs(tweet)
		delete_favs(tweet)
		deleted += 1
except Exception as e:
	print(f"{deleted} tweets deleted.")
	with open('like','r') as new_likes:
		for like in likes:
			new_likes.write(like + '\n')
		print(e)
'''
