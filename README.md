# wordsearch
A word-search solution finder.

By default it uses `/usr/share/dict/words` as the wordlist finding any
word (3 characters or longer) in a wordsearch puzzle.

```
Usage: wordsearch [options] puzzle.txt

Options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary=DICTIONARY
                        Specify an alternate dictionary (one word per line)

  Search options:
    --no-diagonals      Disallow diagonals
    --no-reverse, --no-backwards
                        Disallow reverse matches
    -l LENGTH, --min-length=LENGTH
                        Set the minimum length of interest (default=3)
```
