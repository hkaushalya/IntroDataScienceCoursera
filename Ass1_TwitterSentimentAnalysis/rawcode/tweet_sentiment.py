import sys
import json
#try: import simplejson as json
#except ImportError: import json

def hw():
    print ('Hello, world! See my magic!')

def loadscores(fp):
    scores = {}
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)        # Convert the score to an integer.

    return scores
    #print scores.items() # Print every (term, score) pair in the dictionary

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


def tweetscore(tw_file, sent_file):
    scores_dic = loadscores(sent_file)
    json_dic   = {}
    scores_lst = []
    sc = 0 #score for each tweet
    
    for line in tw_file:
        sc = 0  #reinit
        json_dic = json.loads(line)
        if 'lang' in json_dic:
            lang = json_dic['lang']
            if (lang == 'en'):        
                unicode_string = json_dic[u'text']
                encoded_string = unicode_string.encode('utf-8')
                #print encoded_string
                sc =  calcscore(encoded_string, scores_dic)

        #print (sc)
        scores_lst.append(sc)
    
    return scores_lst

def lines(fp):
    #print str(len(fp.readlines()))
    print ('Lines in ', fp.name, ':', str(len(fp.readlines())) )

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    #hw()
    #lines(sent_file)
    #lines(tweet_file)
    sent_file.seek(0)  # reset the file pointer at the first byte
    tweet_file.seek(0)
    tweetscore(tweet_file, sent_file)

if __name__ == '__main__':
    main()
