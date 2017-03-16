# CS122 W'17: Markov models and hash tables
# YOUR NAME HERE

import sys
import math
import Hash_Table as HT

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        ### YOUR CODE HERE ###
        self.ngram=None
        self.npcgram=None
        ngram=HT.Hash_Table(math.ceil(len(s)/k),False)
        npcgram=HT.Hash_Table(math.ceil(len(s)/k),False)
        for i in range(len(s)-k+1):
            key1=(s*3)[i:i+k]
            value1=ngram.lookup(key1)
            key2=(s*3)[i:i+k+1]
            value2=ngram.lookup(key2)
            if not value1:
                ngram.update(key1,1)
            else:
                ngram.update(key1,value1+1)
            if not value2:
                npcgram.update(key2,1)
            else:
                ngram.update(key1,value2+1)				
        self.ngram=ngram
        self.npcgram=npcgram
        self.k=k
        self.S=len(set(s))
		
    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        ### YOUR CODE HERE ###
        ngram=self.ngram
        npcgram=self.npcgram
        k=self.k+1
        S=self.S
        log_prob=[0]*len(s)
        for i in range(len(s)):
            c=s[i]
            if i-k<0:
                 kc=s[i-k:]+s[:i]
            else:     
                 kc=s[i-k:i]
            log_prob[i]=math.log((npcgram.lookup(kc)+1)/(ngram.lookup(c)+S)) 

        return sum(log_prob)

def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the speakers
    uttering that text under a "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    ### YOUR CODE HERE ###
    m1=Markov(order,speech1)
    m2=Markov(order,speech2)
    p1=m1.log_probability(speech3)/len(speech3)
    p2=m2.log_probability(speech3)/len(speech3)
    conclusion = 'A' if p1>p2 else 'either' if p1==p2 else 'B'
    return (p1,p2,conclusion)	
	

def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)

