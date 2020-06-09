import re

txt = "Hello For other world!"

result = re.search(r"f.r", txt, re.IGNORECASE) # Case sensitive

print(result)

print("Span:", re.search(r"[a-zA-z0-9]unt", "Aunt").span())

result = re.search(r"[^A-Za-z0-9 ]", txt) # wont match any number or alpha neigther a white space

print(result)

result = re.search(r"for|world", txt, re.IGNORECASE) # | or
# re.findall() to find them both
print(result)

result = re.search(r"H.*d", txt, re.IGNORECASE) # Greedy Search

print(result)

# make it less Greedy

result = re.search(r"H[A-Za-z]*d", txt, re.IGNORECASE) # Less Greedy Search

print(result)

result = re.search(r"l+o+", "helloo") # Repetition Search

print(result)

result = re.search(r"h?ello", "hello") # Means Wheter there is h or not (0 or 1) e.g. [ello, hello]

print(result)

result = re.search(r"\.com", "trello.com") # Escape special characters

print(result)


########## Escape Characters #####################################
#	\w : Is identifier - Digits									 #
#	\d : Matching Digits 										 #
#	\s : Matching White Space Characters {Space, Tabs, NewLine}  #
#	\b : For word Boundaries									 #
##################################################################

re.search(r"^A.*a$", "America") # Strict Search Pattern

# Handle Repetition
re.findall(r"[A-Za-z]{5}", "a ghost appears") # Not Limited
re.findall(r"\b[A-Za-z]{5}\b", "a ghost appears") # Limited

# Handle Range Repetition
re.findall(r"[A-Za-z]{5, 10}", "a ghost appears") # Not Limited

# Imagine we want to capture a number inside square brackets
def capture_number(txt):
	regex = r"\[(\d+)\]"
	result = re.search(regex, txt)
	if result is None:
	    return "Nope"
	return result[1]

capture_number("Hello form python handler [1548461]")


# Advanced Spliting

re.split(r"[,.?]", "Hello, Go. No?") # returns a list of splited items
#=> ["Hello", "Go", "No"]
re.split(r"[,.?]", "Hello, Go. No?") # Capturing all as list of splited group items
#=> ["Hello", ",", "Go", ".", "No", "?", ""]

# General Expression for regex
re.sub(r"^([\w .-]*), ([\w.-]*)$", r"\2 \1", "Lastname, Firstname")
# the second expression is to sort the result


