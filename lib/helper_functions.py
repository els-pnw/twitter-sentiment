import json
import numpy as np

def flatten_tweets(tweets_json):
    """ Flattens out tweet dictionaries so relevant JSON
        is in a top-level dictionary.
        
        Borrowed from datacamp, with modification to support
        tweepy.Cursor api.search
        
        Parameters
        ----------
        tweets_json : list
                      A list of tweets in dict (json) format.
        
        Returns
        -------
        tweets_list : list
                      List of tweets in dict (json) format."""
    tweets_list = []
    
    # Iterate through each tweet
    for tweet in tweets_json:
        tweet_obj = json.loads(tweet)
    
        # Store the user screen name in 'user-screen_name'
        tweet_obj['user-screen_name'] = tweet_obj['user']['screen_name']
    
        # Check if this is a 140+ character tweet
        if 'extended_tweet' in tweet_obj:
            # Store the extended tweet text in 'extended_tweet-full_text'
            tweet_obj['extended_tweet-full_text'] = tweet_obj['extended_tweet']['full_text']
    
        if 'retweeted_status' in tweet_obj:
            # Store the retweet user screen name in 'retweeted_status-user-screen_name'
            tweet_obj['retweeted_status-user-screen_name'] = tweet_obj['retweeted_status']['user']['screen_name']

            # Store the retweet text in 'retweeted_status-text'
            if 'text' in tweet_obj['retweeted_status']:
                tweet_obj['retweeted_status-text'] = tweet_obj['retweeted_status']['text']
            elif 'full_text' in tweet_obj['retweeted_status']:
                tweet_obj['retweeted_status-full_text'] = tweet_obj['retweeted_status']['full_text']

        if 'user' in tweet_obj:
            tweet_obj['user-location'] = tweet_obj['user']['location']
            
        tweets_list.append(tweet_obj)
    return tweets_list

def getBoundingBox(place):
    """ Returns the bounding box coordinates.
    
    Borrowed from DataCamp, and tweaked to support NoneType
    
    Parameters
    ----------
    place : dict
            Dictionary from tweet['place']
    
    Returns
    -------
    coordinates : list
                  long and lat coordinates, bounding box."""
    
    if place:
        return place['bounding_box']['coordinates']

def calculateCentroid(place):
    """ Calculates the centroid from a bounding box.
    
    Borrowed from DataCamp, tweaked to support NoneType
    
    Parameters
    ----------
    
    Returns
    -------
    central_long : 
                    
    central_lat :
                    
    """
    # Obtain the coordinates from the bounding box.
    if place is not None:
        coordinates = place['bounding_box']['coordinates'][0]

        longs = np.unique( [x[0] for x in coordinates] )
        lats  = np.unique( [x[1] for x in coordinates] )

        if len(longs) == 1 and len(lats) == 1:
            # return a single coordinate
            return (longs[0], lats[0])
        elif len(longs) == 2 and len(lats) == 2:
            # If we have two longs and lats, we have a box.
            central_long = np.sum(longs) / 2
            central_lat  = np.sum(lats) / 2
        else:
            raise ValueError("Non-rectangular polygon not supported: %s" % 
                ",".join(map(lambda x: str(x), coordinates)) )

        return (central_long, central_lat)
    else:
        return (None, None)