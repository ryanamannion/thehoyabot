#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
generate.py

Ryan Mannion
ram321@georgetown.edu
twitter @ryanamannion
ryanamannion.com

Adapted from code by Amir Zeldes

"""

from random import choice, random
from nltk import word_tokenize
import re
import pickle
import os, sys

# USE IF YOU DO NOT HAVE A PICKLED DICTIONARY
# def get_counts(context_length, training_text):
#     """
#     This function counts the frequencies of all continuations of each context tuple
#     :param context_length: Integer, number of tokens preceding current token (use 2 for trigrams)
#     :param training_text: The training data as one big string
#     :return: counts: A dictionary of context tuples to dictionaries of continuation probabilities
#     """
#
#     counts = {}
#
#     tokens = word_tokenize(training_text)
#     for i in range(len(tokens) - context_length):   # says how many times we want to move that window in the text
#         context = []
#         next_token = tokens[i + context_length]
#
#         for j in range(context_length):
#             context.append(tokens[i + j])
#
#         # Add 1 to frequency or create new dictionary item for this tuple
#         if tuple(context) in counts:
#             if next_token in counts[tuple(context)]:
#                 counts[tuple(context)][next_token] += 1     # when next_token is in counts[tuple(context)] uptick by 1
#             else:
#                 counts[tuple(context)][next_token] = 1      # otherwise make a new one and set it to 1
#         else:
#             counts[tuple(context)] = {next_token: 1}
#
#     return counts


def load_obj(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def detokenize(input):
    """
    This function is meant to detokenize strings of tokens created by nltk.word_tokenize
    :param input: string of tokens separated by whitespace
    :return: string of words as normally seen in English
    """

    input = re.sub(r'(\s)(’)(\s)(s|S)', r'\2\4', input)          # fixes possessive s
    input = re.sub(r'(s|S)(\s)(’)', r'\1\3', input)              # fixes plural possessive s
    input = re.sub(r'(\s)(’)(\s)(re|ll|t|ve)', r'\2\4', input)   # fixes 're 'll 't 've contractions
    input = re.sub(r'(\s)(’)(\s)(Cuse)', r'\2\4', input)         # fixes (Syra)'Cuse contraction
    input = re.sub(r'(O|D)(\s)(’)(\s)', r'\1\3\4', input)        # fixes Irishmen and Italians
    input = re.sub(r'(\s)(,)(\s)', r'\2\3', input)               # fixes commas
    input = re.sub(r'(\s)(\.|\!|\?)', r'\2', input)              # fixes sentence final punctuation
    input = re.sub(r'(\s)(:|;)', r'\2', input)                   # fixes (semi)colons
    input = re.sub(r'(‘|“)(\s)(.*)(\s)(”|’)', r'\1\3\5', input)  # fixes quotes

    return input


def generate(output_length=8):

    counts = load_obj(os.path.join(sys.path[0], 'counts.pkl'))

    """
    this part is a little messy but it works. Comments for clarification
    """

    first_tokens = choice(list(counts.keys()))  # Choose a random first context

    stop_list_begin = ['s', "’", ",", ":", ";", "&"]

    cap_list_begin = ['of', 'in', 'on', 'to', 'the', 'for', 'not', 'and']

    stop_list_end = ['The', 'the', 'in', ':', 'of', 'a', 'to', 'on', "‘", "“", "&", "Every", "With", "and", 'for', 'at']

    if first_tokens[0] in stop_list_begin:
        first_tokens = choice(list(counts.keys()))

    output_list = list(first_tokens)

    if output_list[0] in cap_list_begin:
        output_list[0] = output_list[0].capitalize()

    current_context = first_tokens

    for i in range(output_length):
        next_context = max(counts[current_context], key=(counts[current_context].get))
        temp = list(current_context)
        temp.pop(0)  # Remove first token in previous context
        temp.append(next_context)  # Add new token for the next context
        next_token = temp[-1]
        next_context = tuple(temp)  # look up new context in dictionary, thus tuple()

        current_context = next_context

        output_list.append(next_token)

    if output_list[-1] in stop_list_end:
        next_context = max(counts[current_context], key=(counts[current_context].get))
        temp = list(current_context)
        temp.pop(0)  # Remove first token in previous context
        temp.append(next_context)  # Add new token for the next context
        next_token = temp[-1]
        output_list.append(next_token)

    if output_list[-1] == r'[.|!|?]':
        sentence = " ".join(output_list)
    elif output_list[-1] == r',':
        re.sub(r'\,', r'', output_list[-1])
        sentence = " ".join(output_list)
    else:
        output_list.append('.')    # gives the output sentence-final period if it does not have one
        sentence = " ".join(output_list)

    sentence = detokenize(sentence)

    return sentence

if __name__ == '__main__':
    generate()
