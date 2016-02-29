#import feedparser 
#import sys
#d = feedparser.parse("http://www.reddit.com/r/python/.rss")
#print d['feed']#gives you everything about the channel(general info)
#print d['entries']#entries is a list 
#print d['feed']['link']
#print d['entries'][0]['links']# entries - is just the different entries that have been made
#print len(d['entries'])
#for entrie in d['entries']:
#    print entrie['title'] + "\n"
#print len(sys.argv)



#------------------------------------------------------------------------------------------------------------------------------------


import feedparser
import time
from subprocess import check_output
import sys
import io 
import codecs


feed_name = 'TRIBUNE'
url = 'http://chicagotribune.feedsportal.com/c/34253/f/622872/index.rss'

#feed_name = sys.argv[1]
#url = sys.argv[2]

db = open("C:\Users\ibotev\Desktop\RssFeed.txt",'w')
db.close()

#db = '/var/www/radio/data/feeds.db'
limit = 12 * 3600 * 1000

#
# function to get the current time
#
current_time_millis = lambda: int(round(time.time() * 1000))
current_timestamp = current_time_millis()

def post_is_in_db(title):
    with open("C:\Users\ibotev\Desktop\RssFeed.txt", 'r') as database:
        for line in database:
            if title in line:
                return True
    return False

# return true if the title is in the database with a timestamp > limit
def post_is_in_db_with_old_timestamp(title):
    with open("C:\Users\ibotev\Desktop\RssFeed.txt", 'r') as database:
        for line in database:
            if title in line:
                ts_as_string = line.split('|', 1)[1]
                ts = long(ts_as_string)
                if current_timestamp - ts > limit:
                    return True
    return False

#
# get the feed data from the url
#
feed = feedparser.parse(url)

#
# figure out which posts to print
#
posts_to_print = []
posts_to_skip = []

for post in feed.entries:
    # if post is already in the database, skip it
    # TODO check the time
    title = post.title
    if post_is_in_db_with_old_timestamp(title):
        posts_to_skip.append(title)
    else:
        posts_to_print.append(title)
    
#
# add all the posts we're going to print to the database with the current timestamp
# (but only if they're not already in there)
#
fil = codecs.open("C:\Users\ibotev\Desktop\RssFeed3.txt",encoding = 'utf-8',mode = 'w+')
#f = io.open("C:\Users\ibotev\Desktop\RssFeed2.txt",'a',encoding='utf-8')
for title in posts_to_print:
    if not post_is_in_db(title):
        print "Writing"
        fil.write(title + "|" + str(current_timestamp) + "\n")
        print "Hey"
fil.close
    
#
# output all of the new posts
#
#fil = codecs.open("C:\Users\ibotev\Desktop\RssFeed3.txt",mode = 'w',encoding = 'utf-8')
count = 1
blockcount = 1
for title in posts_to_print:
    if count % 5 == 1:
        print("\n" + time.strftime("%a, %b %d %I:%M %p") + '  ((( ' + feed_name + ' - ' + str(blockcount) + ' )))')
        print("-----------------------------------------\n")
        blockcount += 1
    print(title + "\n")
    title.encode("utf-8")
    count += 1
