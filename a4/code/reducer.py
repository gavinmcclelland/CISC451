#!/usr/bin/env python
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
# input comes from STDIN
for line in sys.stdin:
	line = line.strip()
	# parse the input from mapper.py
	word, count = line.split('\t', 1)
	# convert count (string) to int
	try:
		count = int(count)
	except ValueError:
		# count was not a number, so
		# ignore/discard this line
		continue

	# read key by key
    	if current_word == word:
        	current_count += count
    	else:
        	if current_word:
            		# write result to STDOUT
            		print '%s\t%s' % (current_word, current_count)
        	current_count = count
        	current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s' % (current_word, current_count)


