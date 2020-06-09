import re
reg = re.compile('[a-zA-Z ]{6,}', re.I)
text, words = 'hi world im here', ['world', 'world']
if text == '':
	print(False)
text = reg.findall(text)[0]
if len(words) == 1:
	print(True if words[0] in text else False)
for word in words:
	if word not in text.split():
		print(False)

if len(words) > 1:
	if len(set(words)) == 1:
		print(False)
	str_indexes = [text.split().index(word) for word in words]
	p = 0
	for i in range(len(str_indexes) - 1):
		if str_indexes[i] < str_indexes[i+1]:
			p += 1
	print(True if p == len(str_indexes) - 1 else False)
	
words_order('hi world im here', ['world', 'here']) == True
words_order('hi world im here', ['here', 'world']) == False
words_order('hi world im here', ['world']) == True
words_order('hi world im here', ['world', 'here', 'hi']) == False
words_order('hi world im here', ['world', 'im', 'here']) == True

	
