import tweepy, sys, random, pickle

try:
	#Twitter credentials
	CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
	CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
	ACCESS_KEY = 'YOUR_ACCESS_KEY'
	ACCESS_SECRET = 'YOUR_ACCESS_SECRET'

	#Setting up the authentication and API for Twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	def main():
		#If using cron job, the path must be placed manually
		numberOfNouns = sum(1 for line in open('finnishnouns.txt', 'r'))
			
		#Create a pickle file for maintaining already used nouns
		pickle_file = open('nounfile.pickle', 'ab')
		try:
			usedNouns = pickle.load(open('nounfile.pickle', 'rb'))
		except EOFError:
			usedNouns = []

		#Get a random noun
		nounIndex = random.randint(0, numberOfNouns-1)
		while nounIndex in usedNouns:
			nounIndex = random.randint(0, numberOfNouns-1)
		
		#If using cron job, the path must be placed manually
		noun = open('finnishnouns.txt', 'r').readlines()[nounIndex].strip()

		#Check if the noun has already been tweeted
		if len(usedNouns) < numberOfNouns:
			usedNouns.append(nounIndex)
			with open ('nounfile.pickle', 'wb') as pickle_file:
				pickle.dump(usedNouns, pickle_file)

		#Form the tweet
		tweet = noun + " on pilalla"
			
		api.update_status(tweet)

	if __name__ == "__main__":
		main()
		
except Exception as e:
    print(e)