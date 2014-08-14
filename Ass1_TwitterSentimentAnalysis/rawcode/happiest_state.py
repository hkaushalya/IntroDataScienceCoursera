import sys
import json
#try: import simplejson as json
#except ImportError: import json

DEBUG = True

STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}



def loadscores(fp):
    scores = {}
    for line in fp:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)        # Convert the score to an integer.

    #if (DEBUG)
        #print scores.items() # Print every (term, score) pair in the dictionary

    return scores

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

def findlocation_using_place(place_dic):
    '''
        if 'location' is not null, try to find location
    '''
    pass

def find_location_using_cdt(cdt_lst):
    '''
        find location based on 'coordinates' if 'location' is null
    '''
    pass


def tweetscore(tw_file, sent_file):
    scores_dic = loadscores(sent_file)
    json_dic   = {}
    scores_lst = []
    sc = 0 #score for each tweet
    state_scores = {}
    for line in tw_file:
        sc = 0  #reinit
        try: json_dic = json.loads(line)
        except ValueError: continue

        if 'lang' in json_dic:
            lang = json_dic[u'lang']
            if (lang.encode('utf-8').find('en') != -1):
                unicode_string = json_dic[u'text']
                encoded_string = unicode_string.encode('utf-8')
                #print encoded_string
                sc =  calcscore(encoded_string, scores_dic)

                # now find location
                place_dic = json_dic[u'place']
                if (not place_dic):
                    continue

                #print place_dic
                country = place_dic[u'country']
                if (country):
                    if ( (country.encode('utf-8').find('US') == -1)
                        and (country.encode('utf-8').find('United States') == -1)
                        ):
                        continue

                state = place_dic[u'name']
                if (not state):
                    continue

                #print (country, ',', state)

                if (state in state_scores.keys()):
                    state_scores[state] += sc
                else:
                    state_scores[state] = sc

    hap_state = ''
    for key, value in sorted(state_scores.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        #print "%s %s" % (key, value)
        hap_state = key
        break
    #return scores_lst


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    tweetscore(tweet_file, sent_file)

if __name__ == '__main__':
    main()
