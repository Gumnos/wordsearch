# wordsearch
A word-search solution finder.

## Usage
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

A puzzle is a text-file with equal-length lines such as

```
$ cat puzzle.txt
jkqcxq
sleety
uybtjx
niarih
nphail
ycoldo
```

If looking for particular words, they can be provided as an alternate
dictionary:

```
$ cat words_to_find.txt
cold
hail
rain
sleet
sunny
```

All words in both the dictionary and the puzzle are normalized to
lowercase before searching.

## Options

By default it uses `/usr/share/dict/words` as the wordlist.
This can be changed using the `-d WORDLIST` option.

By default it will look for words diagonally, including backwards.
These can be disabled by using the `--no-diagonals` and `--no-backwards`
options.

Additionally, words in the word-list shorter than 3 letters are ignored
by default.
The `-l LENGTH` option allows this to be changed.
This is more useful when using a large dictionary rather than a list of
words expected to be found in the puzzle.

Examples:

Typical usage of finding a word-list `words_to_find.txt` in a given
puzzle `puzzle.txt`:

```
$ python wordsearch.py -d words_to_find.txt puzzle.txt
```

Find all words of length 2 or more from the system dictionary:

```
$ python wordsearch.py -l 2 puzzle.txt
```

Find only words that don't require going up or left

```
$ python wordsearch.py --no-backwards puzzle.txt
```

Find only words in `words_to_find.txt`  that don't require going up or left, and don't include
diagonals

```
$ python wordsearch.py --no-diagonals --no-backwards -d words_to_find.txt puzzle.txt
```
