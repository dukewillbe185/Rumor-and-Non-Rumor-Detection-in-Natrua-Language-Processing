import tweepy
import json


def authenticate(BEARER_TOKEN):

    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)

    return client


def fetch_tweet(client, id):

    tweet = {}
    response = client.get_tweets(id, 
                                tweet_fields = ['attachments', 'created_at', 'entities', 'geo', 
                                                'public_metrics', 'referenced_tweets', 
                                                'author_id', 'source', 'context_annotations', 'in_reply_to_user_id', 'lang'],
                                place_fields = ['geo', 'country', 'name', 'place_type'],
                                user_fields = ['created_at', 'description','entities', 'public_metrics', 'verified'],
                                media_fields = ['url', 'duration_ms', 'public_metrics', 'alt_text'],
                                expansions = 'geo.place_id,author_id,attachments.media_keys,in_reply_to_user_id')
    try:
        if response.data is not None:
            for t in response.data:
                tweet.update(t.data)
    except Exception as e:
        print(f'Exception for tweet: {e}')
        pass
    try:
        if response.includes.get('users', None) is not None:   
            for user in response.includes['users']:
                tweet['user'] = user.data
    except Exception as e:
        print(f'Exception for users: {e}')
        pass
    try:
        if response.includes.get('place', None) is not None:
            for place in response.includes['place']:
                tweet.update(place.data)
    except Exception as e:
        print(f'Exception for place: {e}')
        pass
    try:
        if response.includes.get('media', None) is not None:
            for media in response.includes['media']:
                tweet.update(media.data)
    except Exception as e:
        print('f Exception for media: {e}')
        pass

    return tweet


def write_to_file(id, tweet, path):
    with open(path + id +'.txt', 'w') as f:
        json.dump(tweet, f)


def tweets_processed(filepath):

    ids = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split(' : ')
            ids.append(line[0])
    return ids


def read_process(client, r_path, w_path, logpath):

    ids = tweets_processed(logpath)   
     
    with open(r_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.strip('\n')
            line = line.split(',')
            for id in line:
                if id not in ids:
                    try:
                    
                        tweet = fetch_tweet(client, id)   

                        write_to_file(id, tweet, w_path)

                        log = id + ' : yes\n'
                        with open('log.txt', 'a') as f:
                            f.write(log)  
                    except Exception as e:
                        print(f'Exception for fetch and write: {e}')
                        print(id)
                        pass
                    

if __name__ == '__main__':

    # BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGvGbQEAAAAACMRCC9dW75oHLdZY872KQV%2FwncY%3DAYzORvis40n3ndPKneBisKPBQ4sYVpNthL0YHJLJZ9d6WmAjWY'
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAAoxbAEAAAAApib47uKVACiyXfOSAj8BELeJaf4%3DT4L0eLVTNooQRZVftkppGGnEoRqau3K2R73ZJYo3jB8TZFghZJ'
    # BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAGjcbAEAAAAAnAt%2FNMSgejEX0q4HaxMGYfwExWU%3DT4mLNCEmm8oJxrCYbGGYDzEvuFwHPr4VHYvrzXJooQLTyeAbe2'

    client = authenticate(BEARER_TOKEN)

    read_process(client, 'chunk-3.txt', 'covid-objects/', 'log.txt')