#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
getcounts.py

This script takes hoyatitles.txt and counts the trigram continuations for use in generate.py. The output of this file
is a pickled dictionary called counts.pkl, which allows generate.py to simply load the counts instead of counting every
time.

Ryan A. Mannion
ram321@georgetown.edu
twitter @ryanamannion
ryanamannion.com

"""

import pickle
import os, sys
from nltk import word_tokenize

def get_counts(context_length, training_text):
    """
    This function counts the frequencies of all continuations of each context tuple
    :param context_length: Integer, number of tokens preceding current token (use 2 for trigrams)
    :param training_text: The training data as one big string
    :return: counts: A dictionary of context tuples to dictionaries of continuation probabilities
    """

    counts = {}

    training_text = open(training_text).read()

    tokens = word_tokenize(training_text)
    for i in range(len(tokens) - context_length):   # says how many times we want to move that window in the text
        context = []
        next_token = tokens[i + context_length]

        for j in range(context_length):
            context.append(tokens[i + j])

        # Add 1 to frequency or create new dictionary item for this tuple
        if tuple(context) in counts:
            if next_token in counts[tuple(context)]:
                counts[tuple(context)][next_token] += 1     # when next_token is in counts[tuple(context)] uptick by 1
            else:
                counts[tuple(context)][next_token] = 1      # otherwise make a new one and set it to 1
        else:
            counts[tuple(context)] = {next_token: 1}

    return counts


d = get_counts(3, os.path.join(sys.path[0], 'hoyatitles.txt'))

pickle.dump(d, open("counts.pkl", "wb"))
