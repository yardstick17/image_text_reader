#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def remove_numeric_part(string):
    no_digits = []
    for i in string:
        if not i.isdigit():
            no_digits.append(i)

    result = ''.join(no_digits)
    return result


def remove_too_many_small_words_dish(text):
    new_text = []
    text = text.split('\n')
    for lines in text:
        word_count = 0.0
        small_word_count = 0.0
        line = lines.split(' ')
        for word in line:
            if len(word) <= 2:
                small_word_count += 1
            word_count += 1
        try:
            small_word_proportion = small_word_count / word_count

        except Exception as E:
            print('got the exception  ', E)
            small_word_proportion = 0.0
        if small_word_proportion <= 0.4:
            new_text.append(line)
    return new_text


def make_string_alphanmeric(lines):
    s = re.sub('[^0-9a-zA-Z\n]+', ' ', lines)
    return s.strip()
