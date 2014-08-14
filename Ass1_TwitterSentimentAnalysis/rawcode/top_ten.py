import sys
#from tweet_sentiment import *
import json

DEBUG = False

def myprocess(tw_file):
    hashtagcount_dic = {}

    for line in tw_file:
        sc = 0
        try: json_dic = json.loads(line)
        except ValueError:
            if (DEBUG):
                print ('Value error in covering json.load. moving to next line ...')

            continue

        if (DEBUG):
            print ('json dic' , ' =======\n', json_dic)

        if 'lang' in json_dic:
            lang = json_dic[u'lang']

            if (DEBUG):
                print ('Language found = ', lang.encode('utf-8'))

            if lang.encode('utf-8').find('en') != -1 :
                ent_dic = json_dic[u'entities']
                tag_lst = ent_dic[u'hashtags']
                if (DEBUG):
                    print (tag_lst)

                if len(tag_lst) == 0:
                    continue

                tags_dic = tag_lst[0]
                hashtag = tags_dic[u'text']
                if (DEBUG):
                    print 'found tags = ', hashtag, '(', type(hashtag),')'

                word = hashtag.encode('utf-8')
                if word in hashtagcount_dic:                # increment counters if existing
                    hashtagcount_dic[word] += 1
                else:                                       # create a new entry
                    hashtagcount_dic[word] = 1
                    #print (word, '->', newterms_dic[word])
            else:
                if (DEBUG):
                    print ('Language is not english. skipping...')
        else:
            if (DEBUG):
                print ('Key word \'lang\' not found. Skipping...')

    count = 0
    #for val in sorted(hashtagcount_dic.itervalues()):
    #print "%s: %s" % (k, mydict[key])

    for key, value in sorted(hashtagcount_dic.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print "%s %s" % (key, value)
        count += 1
        if (count==10):
            break

    #for k, v in hashtagcount_dic.iteritems():
        #print k, ' ', v
        #count10 += 1
        #if (count10 == 10):
            #break


def main():
    tweet_file = open(sys.argv[1])
    myprocess(tweet_file)


if __name__ == '__main__':
    main()
