import sys
#from tweet_sentiment import *
import json

def myprocess(tw_file):
    newterms_dic = {}

    for line in tw_file:
        sc = 0
        try: json_dic = json.loads(line)
        except ValueError: continue

        if 'lang' in json_dic:
            lang = json_dic['lang']

            if lang == 'en':
                unicode_string = json_dic[u'text']
                encoded_string = unicode_string.encode('utf-8')

                for word in encoded_string.lower().split(' '):
                    if not word.isalpha():         #skip words with non alphabetic characters
                        continue

                    if word not in newterms_dic:                # create a new entry
                        newterms_dic[word] = 1
                    else:                                       # increment counters if existing
                        newterms_dic[word] += 1
                        #print (word, '->', newterms_dic[word])

    for k, v in newterms_dic.iteritems():
        print k, ' ', v


def main():
    tweet_file = open(sys.argv[1])
    myprocess(tweet_file)


if __name__ == '__main__':
    main()
