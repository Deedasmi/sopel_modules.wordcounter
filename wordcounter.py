# coding=utf8
"""
wordcounter.py - Simple word counter for Sopel
Copyright © 2015, Richard Petrie, <rap1011@ksu.edu>
Licensed Eiffel Forum License, version 2
"""

from __future__ import unicode_literals
from sopel.module import commands, example, NOLIMIT, rule
import re
import heapq
import csv

user_words = {}
all_words = {}

STOP_WORDS = set([])

IGNORE = ["!", ",", "?", "*", ".", "<", ">", "(", ")"]

@rule(".*")
def log_words(bot, trigger):
    """
    Logs all words that are said
    """
    user = trigger.nick.upper()
    sentence = trigger.group(0)

    if user == bot.nick or ".words" in sentence:
        return NOLIMIT

    for char in IGNORE:
        sentence = sentence.replace(char, "")

    words = sentence.split()
    for word in words:
        if word in STOP_WORDS:
            continue
        if word not in all_words:
            all_words[word] = 0
        if user not in user_words:
            user_words[user] = {}
        if word not in user_words[user]:
            user_words[user][word] = 0
        all_words[word] += 1
        user_words[user][word] += 1


@commands("words")
def words(bot, trigger):
    try:
        user = trigger.group(2).split()[0]
        use = user_words[user.upper()]
    except(KeyError, AttributeError, TypeError):
        use = all_words

    number = 5
    ignore_rules = False

    try:
        if "-i" in trigger.group(2):
            ignore_rules = True
    except (AttributeError, TypeError):
        pass

    try:
        find_number = re.search(r'-n\s([0-9])', trigger.group(2))
        if find_number:
            number = int(find_number.group(1))
    except (AttributeError, TypeError):
        pass

    string = format_string(get_top(use, number, ignore_rules), use)
    bot.say(string)


def get_top(use_dict, number, ignore_rules):
    if ignore_rules:
        use_dict = use_dict.copy()
        del_keys = []
        for key in use_dict.keys():
            if len(key) < 4:
                del_keys.append(key)
        for key in del_keys:
            del use_dict[key]

    return  heapq.nlargest(number, use_dict, use_dict.get)


def format_string(top_list, use_dict = all_words):
    response = ""
    for item in top_list:
        response += "'{}' : {}, ".format(item, use_dict[item])
    return response[:-2]

def get_stop_words():
    with open('stop-word-list.csv', newline='') as f:
        reader = csv.reader(f)
        for item in reader:
            STOP_WORDS.add(item)

get_stop_words()