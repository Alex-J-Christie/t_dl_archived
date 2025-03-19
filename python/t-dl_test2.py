import tweepy
import youtube_dl
import argparse
from slugify import slugify

#Arguments for program
parser = argparse.ArgumentParser(description='a program for downloading every video within a twitter users likes.')
parser.add_argument("-u", "--user", help="sets the target user")
#parser.add_argument("-a", "--amount", help="sets the amount of tweets to download.", type=int)
args = parser.parse_args()

#print(args.user)

#Needed Tokens
consumer_key = open("consumer_key.txt", "r")
consumer_secret = open("consumer_secret.txt", "r")
access_token = open("access_token.txt", "r")
access_token_secret = open("access_token_secret", "r")
bearer_token = open("bearer_token.txt", "r")


#Tweepy Authentication
client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

#Takes in -u input to decide whose likes we steal and download >:) (Which means just my tweets)
#just makes the input into a nice format for auth converts usernames to IDs
user_input = args.user
if user_input[0] == "@":
    user_input = user_input[1:]

username = client.get_user(username=user_input)
user_id = username.data.id

#Pulls the tweet data, organizes by name and video link, then prints them
counted = False
current_list = None
api_text_list = []


while counted == False:
    tweets = client.get_liked_tweets(user_id, pagination_token=current_list)
    total_tweets = tweets.meta['result_count']
    
    if total_tweets == 0:
        counted = True
    
    for i in range(total_tweets):
        
        amount_of_links = 1

        txt = tweets.data[i].text
        print(txt)
        first_video_position = txt.find('https://t.co/')
        first_link_cut = txt[first_video_position:(first_video_position + 23)]
        print("first link cut is: " + str(first_link_cut))
        alt_txt_1 = txt.replace(first_link_cut, '')

        if alt_txt_1.find('https://t.co/') != -1:
            amount_of_links = 2
            second_link_cut = alt_txt_1[alt_txt_1.find('https://t.co/'):(alt_txt_1.find('https://t.co/') + 23)]
            alt_txt_2 = alt_txt_1.replace(second_link_cut, '')
            print("alt_txt_2 is: " + str(alt_txt_2))
            print("amount of links is: " + str(amount_of_links))

        print("alt_txt_1 is: " + str(alt_txt_1))
        print("There are: " + str(amount_of_links) + " links in this tweet")
        final_name = ''

        if amount_of_links == 2 and len(alt_txt_2) >= 4:
            final_name = slugify(alt_txt_2, allow_unicode=True, separator=" ")
            print("chose second name and alt text 2 length is: " + str(len(alt_txt_2)))
        elif len(alt_txt_1) == 0:
            final_name = tweets.data[i].id
            print("tweet data id is: " + str(tweets.data[i].id))
#        elif len(alt_txt_2) == 0:
#            final_name = tweets.data[i].id
#            print("tweet data id is: " + str(tweets.data[i].id))         
        else:
            final_name = slugify(alt_txt_1, allow_unicode=True, separator=" ")

        if len(str(final_name)) > 240:
            final_name = final_name[:239]

        print("final name is: " + str(final_name))

        ydl_opts = {
        'outtmpl': (str(final_name) + '.mp4'),
        'ignoreerrors': True,
        }   

        if amount_of_links == 2:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("**********downloading first link cut: " + str(first_link_cut))
                ydl.download([first_link_cut])
                print("**********downloading second link cut: " + str(second_link_cut))
                ydl.download([second_link_cut])
        else:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("**********downloading first link cut: " + str(first_link_cut))
                ydl.download([first_link_cut])

        for i in range(5):
            print(" ")

        if (i + 1) == total_tweets:
            current_list = tweets.meta['next_token']
            pass


#quick test
test_counted = False
while test_counted == False:
    tweets = client.get_liked_tweets(user_id, pagination_token=current_list)
    total_tweets_t = tweets.meta['result_count']
    
    if total_tweets_t == 0:
        test_counted = True
    
    for i in range(total_tweets):
        print(tweets.data[i].text)

consumer_key.close()
consumer_secret.close()
access_token.close()
access_token.close()
bearer_token.close()

