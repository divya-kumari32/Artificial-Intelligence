############################################################
# CIS 521: Language Models Homework 
############################################################

student_name = "Divya Kumari"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import re
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    words = re.findall(r"[\w]+|[^\s\w]", text)  #regex to split tokens including punctuation
    return words

def ngrams(n, tokens):
    tokens_padded = ["<START>"] * (n-1) + tokens + ["<END>"]    #pad the tokens to create ngrams string

    ngram = []
    start = 0
    prefix_tokens = []

    #numbering the token so to keep track of the padded context and token combinations
    prefix_tokens += [(start+i, tokens_padded[i]) for i in range(len(tokens_padded))]

    start = 0

    #appending the tuple of padded context up until that point and the token
    for i, token in prefix_tokens:
        if (n-1) <= i:
            start = (i-n)+1
            ngram.append((tuple(tokens_padded[start:i]), token))

    return ngram

class NgramModel(object):

    def __init__(self, n):
        self.n = n  #n grams
        self.context_count = dict() #internal variable to count of the context
        self.context_token_count = dict()  #internal variable to count of the context and token

    def update(self, sentence):
        tokens = tokenize(sentence) #get all tokens from the sentence
        
        computed_ngrams = ngrams(self.n, tokens) #get all computed ngram values
        for context, token in computed_ngrams:
            #counter 1: updating dictionary only for contexts
            if context not in self.context_count:
                self.context_count[context] = 1     #update count if context doesn't exist yet
            else:
                self.context_count[context] += 1       #update count if context is repeated

            #counter 2: updating dictionary for contexts and token combinations
            if context not in self.context_token_count:
                self.context_token_count[context] = {token : 1}     #update count if context doesn't exist yet
            else:
                if token not in self.context_token_count[context]:
                    self.context_token_count[context][token] = 1      #update count if context is repeated and token for that context doesn't exist yet
                else:
                    self.context_token_count[context][token] += 1   #update count if context and token for that context is repeated
            

    def prob(self, context, token):
        if context in self.context_token_count and token in self.context_token_count[context]:
            prob = float(self.context_token_count[context][token]) / self.context_count[context]    #returns probability of that context-token combination occuring given that the context occurs
            return prob
        else:
            return 0

    def random_token(self, context):
        r = random.random()     #random variable to calculate probability
        if context in self.context_count:
            #sort the tokens according to context in lexicographic orderin
            context_token = sorted(
                self.context_token_count[context].keys())    
        
        floor = 0
        ceil = 0
        for token in context_token:
            ceil += self.prob(context, token)   #calculate the max probability of the context-token pair
            if floor <= r < ceil:
                return token        #return token if r is in between the min and max probability

            floor += self.prob(context, token)      #calculate the min probability of the context-token pair

        return None


    def random_text(self, token_count):
        tokens = []

        if self.n == 1:     #if n is just append and update the tokens
            for i in range(token_count):
                tokens.append(self.random_token(()))
        else:
            curr_context = ("<START>",) * (self.n-1)    #set starting context
            for i in range(token_count):
                curr_token = self.random_token(curr_context)
                tokens.append(curr_token)   #if n > 1, calculate and update random tokens after running random_token fn

                if curr_token == "<END>":      #if token is <END>, reset the context to starting context
                    curr_context = ("<START>",) * (self.n-1)
                else:
                    curr_context = curr_context[1:] + (curr_token,)     #else, set current context to current context-token pair

        return " ".join(tokens)         #return space separated tokens

    def perplexity(self, sentence):
        sum = 0
        tokens = tokenize(sentence)     #tokenize the sentence

        #calculate the current model according to formula after ngrams are computed
        for curr_context, token in ngrams(self.n, tokens):
            sum += math.log(self.prob(curr_context, token))

        #caclulate perplexity value according to current bigram model
        perplexity_value = (1/math.exp(sum)) ** (float(1)/(len(tokens)+1))

        return perplexity_value #return value

def create_ngram_model(n, path):
    ngram = NgramModel(n)

    with open(path) as f:
        for l in f:
            ngram.update(l)

    return ngram

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = 8

feedback_question_2 = """
Understanding the assignment and what it wanted by following the assignment language was a little hard to follow. 
Would have been even tougher if there were no recordings to go back to and listen. 
"""

feedback_question_3 = """
I had studied n gram theory in big data so it was fun to see it come to use and code it even
"""
