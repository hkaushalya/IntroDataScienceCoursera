import sys
#from tweet_sentiment import *
import json

def hw():
    print ('Hello, world!')


def lines(fp):
    print (str(len(fp.readlines())))
    #print 'Lines in ', fp.name(), ':', str(len(fp.readlines()))

def calcscore(s_str, scores_dic):
    twt_score_int = 0

    #print s_str
    for wd in s_str.split(' '):
        word = wd.lower()
        #print 'looking score for ', word.lower()
        #print scores.keys()
        if word in scores_dic.keys():
            sc = scores_dic[word]
            twt_score_int += sc
            #print word , ' found in dic with score of ', sc

    #print 'total score = ', twt_score
    return twt_score_int

def loadscores(fp):
    scores = {}
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)        # Convert the score to an integer.

    return scores
    #print scores.items() # Print every (term, score) pair in the dictionary

def myprocess(tw_file, st_file):
    #get the sentiment score dic
    sent_dic = loadscores(st_file)
    ignore_lst = ['@','http', ' ', '%', '#',',', '~', '\t', '*', '&']

    # now find the score for each tweet and generate
    # a new dictionary with the words that are not present.
    # newterms_dict{"term":[num. of -ve twts, num. of neutral twts, num. of +ve twts,]}
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

                sc = calcscore(encoded_string, sent_dic)
                #print(encoded_string)
                #print('score = ', sc)

                newterm_count = [0, 0, 0]
                if (sc < 0):
                    newterm_count[0] = 1
                elif (sc == 0):
                    newterm_count[1] = 1
                elif (sc > 0):
                    newterm_count[2] = 1

                #print 'newterm_vec = ', newterm_count

                # now generate the new terms dict
                for word in encoded_string.lower().split(' '):
                    if not word.isalpha():         #skip words with non alphabetic characters
                        continue

                    if word not in sent_dic:
                        if word not in newterms_dic:                # create a new entry
                            newterms_dic[word] = newterm_count
                        else:                                       # increment counters if existing
                            for i in range(len(newterms_dic[word])):
                                newterms_dic[word][i] += newterm_count[i]


    #print(' -------------- NEW TERMS DICTIONARY --------------- ')
    #print(newterms_dic.items())

    # need to normalized the newterms scores
    for k,v in newterms_dic.iteritems():
        #print (k, '->', v)
        v_int = map(int, v)  # cast list of strings to int
        tot   = sum(v_int)
        #max_item_index = v_int.index(max())
        #print ('tot=',tot)
        #new_v      = 0 if (tot==0) else [float(x)/float(tot) for x in v_int]

        #term_score = 0 if tot==0 else float(v_int[0]-v_int[2])/float(tot)  # (+ve - -ve)/tot
        #term_score = round(term_score,4)
        term_score = 0 if v_int[0] == 0 else float(v_int[2])/float(v_int[0])
        # 0<term_score<1 is -ve
        # term_score>1 is +ve
        # lets center this around 0
        # must prevent neutral terms being forced
        term = str(k)
        print term,' ',term_score


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    sent_file.seek(0)
    tweet_file.seek(0)
    myprocess(tweet_file, sent_file)


if __name__ == '__main__':
    main()
