#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
import random
import pickle

try:
    # Twitter credentials
    CONSUMER_KEY: str = "YOUR_CONSUMER_KEY"
    CONSUMER_SECRET: str = "YOUR_CONSUMER_SECRET"
    ACCESS_KEY: str = "YOUR_ACCESS_KEY"
    ACCESS_SECRET: str = "YOUR_ACCESS_SECRET"

    # Setting up the authentication and API for Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    def main():
        # If using cron job, the path must be placed manually
        number_of_nouns: int = sum(1 for line in open("finnishnouns.txt", "r"))

        # Create a pickle file for maintaining already used nouns
        pickle_file = open("nounfile.pickle", "ab")
        try:
            used_nouns: list = pickle.load(open("nounfile.pickle", "rb"))
        except EOFError:
            used_nouns: list = []

        # Get a random noun
        noun_index: int = random.randint(0, number_of_nouns - 1)
        while noun_index in used_nouns:
            noun_index = random.randint(0, number_of_nouns - 1)

        # If using cron job, the path must be placed manually
        noun: str = open("finnishnouns.txt", "r").readlines()[noun_index].strip()

        # Check if the noun has already been tweeted
        if len(used_nouns) < number_of_nouns:
            used_nouns.append(noun_index)
            with open("nounfile.pickle", "wb") as pickle_file:
                pickle.dump(used_nouns, pickle_file)

        # Form the tweet
        tweet: str = noun + " on pilalla"

        api.update_status(tweet)

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e)
