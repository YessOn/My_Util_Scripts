# Try the code: https://pythex.org/
# CheatSheet: https://www.debuggex.com/cheatsheet/regex/python

import re

# Quantifiers
# *, +, ?, {interval}

txt = "Alias of Number +212-604251452"
my_phone = re.search(r"\+\d{3}-\d{9}", txt)

# print(txt[my_phone.span()[0]:my_phone.span()[1]])
print(my_phone.group())

# Character Classes
# [A-z0-9] All Letters & Digits
# [^A-Z] Not Capital Letters
# [\b] Backspace Character
# \w One Word
# \W One Non-Word
# \d One Digit
# \D One Non-Digit

txt = "Hola UR 146 abc"
my_search = re.search(r"\s[A-Z]{2}\s[0-9]{3}\s\w{,6}", txt)
print(my_search.group())

# Assertions
# ^ Starts With
# $ Ends With

txt = "+212-604251452"
my_result = re.findall(r"^\+\d{3}-?\d{9}$", txt)
print(my_result[0])


# Match Mails
txt = """
abcdef@gmail.com
abcd1454@mail.ru
yank.revol@hotmail.fr
yank_revol@hotmail.fr
"""
my_result = re.findall(r"[A-z0-9\.]+@[A-z]+\.[A-z]+", txt)
print(my_result)

# Groups
# () Grouping Items

# Capturing Urls
txt = """
http://www.google.com
http://youtube.com
https://gmail.com
"""
my_result = re.findall(r"(https?://)(www\.)?([A-z0-9]+\.)(com|net|info)", txt)
print(my_result)

# Flags
# re.DOTALL : Solves the problem of the . when \n new line
# re.VERBOSE : Write Comments into the regex
# re.I : Ignore, Case sensitive
# re.MULTILINE : Multiline search, Solves the problem of ^[A-z]+$
