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


def make_string_alphanmeric(lines):
    s = re.sub('^[a-zA-Z0-9\\-\\s]+$', ' ', lines)
    return s.strip()


class CleanText(object):
    def __init__(self, text):
        self.text = text

    def process(self):
        return make_string_alphanmeric(self.text)
