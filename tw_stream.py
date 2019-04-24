from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import conn
import sentiment
from datetime import datetime

# credentials initial
__credentials__ = {}

__db_cli__ = None

class listener(StreamListener):
    # https://twitter.com/<username>/status/<id>
    def on_data(self, data):
        try:
            data = json.loads(data)
            if data["lang"] == "en":
                positive, negative = sentiment.get_sentiments(data["text"])
                for keyword in __credentials__["twitter"]["filters"]:
                    if data["text"].lower().find( keyword.lower() ) != -1:
                        conn.insert_to(
                            __db_cli__,
                            __credentials__["mongodb"]["database"],
                            "twitter",
                            {
                                "url": "https://twitter.com/%s/status/%s"%(data["user"]["screen_name"], data["id_str"]),
                                "username": data["user"]["screen_name"],
                                "tweet": data["text"],
                                "positive": positive,
                                "negative": negative,
                                "sentiment": True if positive >= negative else False,
                                "date": datetime.now(),
                                "keyword":keyword
                            }
                        )
            else:
                pass#fail

        except Exception as e:
            print(e)
        return True

    def on_error(self, status):
        print(status)


## loading creds json file
def load_creds():# 
    with open("creds.json","r") as foo:
        data = foo.read()

    try:
        # parse the json file
        return json.loads(data)
    except Exception as e:
        print("Can't parse the creds.json file\n", e)
        # return None if parse is failed

def start_streaming():
    global __credentials__

    auth = OAuthHandler(
        __credentials__["twitter"]["api"]["key"], 
        __credentials__["twitter"]["api"]["secret"]
    )

    auth.set_access_token(
        __credentials__["twitter"]["token"]["token"], 
        __credentials__["twitter"]["token"]["secret"]
    )

    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=__credentials__["twitter"]["filters"])

if __name__ == '__main__':
    __credentials__ = load_creds()
    __db_cli__ = conn.get_client(
        __credentials__["mongodb"]["username"],
        __credentials__["mongodb"]["password"],
        __credentials__["mongodb"]["host"],
        __credentials__["mongodb"]["port"],
        __credentials__["mongodb"]["database"]
    )
    print("connection established")

    start_streaming()






