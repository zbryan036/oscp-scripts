#!/usr/bin/python3
import sys
import os
import re

# Generate a custom wordlist for password attacks based on the contents of a text file

######## DEFINITIONS ########
def print_help():
    print('''Generates a wordlist based on the provided input file

    gwordl.py [OPTIONS] infile outfile

If outfile is \'stdout\', passwords will be printed to stdout. --help
and --verbose output are printed to stderr, and will not interfere with
redirection

OPTIONS

    -v, --verbose         It do what it say it do
    --max=<int>           Passwords longer than --max will be ignored.
                            Default is 15.
    --min=<int>           Passwords shorter than --min will be ignored,
                            and will not be concatenated with anything.
                            low numbers will drastically increase
                            output. Default is 4.
    --short=<int>         Passwords with length --short or less will be
                            concatenated with all other short passwords.
                            High numbers will drastically increase
                            output. Default is 3. If --short is less than
                            --min, no concatenations will be made.
    -r, --retain-case     normal behavior is to make all words
                            lowercase; with -r, case is maintained.
    -s, --special-chars   keep special characters; normally they are
                            discarded
''', file=sys.stderr)
    exit()

def add_to_output_words(word):
    if lowercase:
        word = word.lower()
    # don't add duplicates
    if word in output_words:
        return
    # don't add numbers, unless they're 4 digits
    if re.match(r'^(\d{1,3}|\d{5,}?)$', word):
        return
    # don't add words longer than max_length, or single-letter words
    if len(word) > max_length or len(word) < min_length:
        return
    output_words.append(word)
    if len(word) <= short_max:
        if verbose:
            print('New short word:', word, file=sys.stderr)
        for short_word in short_words:
            add_to_output_words(word + short_word)
            add_to_output_words(short_word + word)
        short_words.append(word)

######## PARSE COMMAND-LINE OPTIONS ########
if len(sys.argv) < 3 or '-h' in sys.argv or '--help' in sys.argv:
    print_help()

# defaults
# TODO verbose prints nothing useful so far
verbose = False
max_length = 15
min_length = 4
short_max = 3
lowercase = True
special_chars = False

options = sys.argv[1:-2]
for option in options:
    if option == '-v' or option == '--verbose':
        verbose = True
    elif option == '-r' or option == '--retain-case':
        lowercase = False
    elif option == '-s' or option == '--special-chars':
        special_chars = True
    elif '--max' in option:
        max_length = int(option.split('=')[1])
    elif '--min' in option:
        min_length = int(option.split('=')[1])
    elif '--short' in option:
        short_max = int(option.split('=')[1])
    else:
        print('[!]', sys.argv[i], 'has not been implemented yet', file=sys.stderr)

outfile = sys.argv[-1]
infile = sys.argv[-2]

if verbose:
    print('infile:', infile, file=sys.stderr)
    print('outfile:', outfile, file=sys.stderr)
    print('lowercase:', lowercase, file=sys.stderr)
    print('special_chars:', special_chars, file=sys.stderr)

if not os.path.isfile(infile):
    print_help()

######## READ INFILE ########
with open(infile) as f:
    full_text = f.read()
# create an array of words from the input
if special_chars:
    input_words = re.findall(r'\S+', full_text)
else:
    input_words = re.findall(r'\w+', full_text)

output_words = []
short_words = []
for word in input_words:
    add_to_output_words(word)

######## WRITE OUTPUT ########
if outfile == 'stdout':
    for word in output_words:
        print(word)
else:
    with open(outfile, 'w') as f:
        for word in output_words:
            f.write(word + '\n')
