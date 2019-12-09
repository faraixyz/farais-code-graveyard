# Retweet Be Gone
A script that can mass delete tweets and likes.

**Note: This repo is no longer being maintained**

## Requirements
* Python 3.6 or higher
* [requests](http://docs.python-requests.org/en/master/)
* [API Keys from Twitter](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html)

## Instructions
1. Get API Keys from twitter and add them to a file called `config.json` at the root of this project
```json
{
    "consumer": {
        "secret": "",
        "key": ""
    },
    "user": {
        "secret": "",
        "key": ""
    }
}
```
2. Open up the Python command line, import the library and call either `delete_favs`, `delete_tweets` or `hide_retweets_from_friends` to wither delete liked tweets, delete tweets or hide tweets from friends respectively.
