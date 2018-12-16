#!/usr/bin/env python

DEFAULT_MIN_LENGTH = 3
class InvalidInput(ValueError): pass

class Puzzle(object):
    SENTINEL = object()

    def __init__(self, data):
        if len(data) < 2:
            raise InvalidInput("Must have more than one row")
        len_1 = len(data[0])
        for i, row in enumerate(data):
            if len(row) != len_1:
                raise InvalidInput("Row %i is not %i long" % (i + 1, len_1))
            for j, c in enumerate(row):
                if len(c) != 1:
                    raise InvalidInput("(%i,%i) not 1 character %r" % (
                        j+1, i+1, c,
                        ))
        self.data = data

    @classmethod
    def build_dictionary(cls, f):
        from_string = isinstance(f, str)
        if from_string:
            f = open(f)
        try:
            results = {}
            for s in f:
                s = s.strip()
                if not s.islower(): continue
                loc = results
                for letter in s.strip():
                    loc = loc.setdefault(letter, {})
                loc[cls.SENTINEL] = True
            return results
        finally:
            if from_string:
                f.close()

    @staticmethod
    def dir_to_desc(dir_row, dir_col):
        if dir_row > 0:
            direction = "south"
        elif dir_row < 0:
            direction = "north"
        else:
            direction = ""
        if dir_col > 0:
            direction += "east"
        elif dir_col < 0:
            direction += "west"
        return direction

    @staticmethod
    def parse_file(f):
        from_string = isinstance(f, str)
        if from_string:
            f = open(f)
        try:
            return [row.strip().lower() for row in f]
        finally:
            if from_string:
                f.close()
        
    def find_words(self, dictionary,
            allow_diagonals=True,
            allow_reverse=True,
            min_length=DEFAULT_MIN_LENGTH,
            ):
        directions = [
            (a,b)
            for a in (-1,0,1)
            for b in (-1,0,1)
            if not (a == 0 and b == 0)
            ]
        if not allow_diagonals:
            directions = [
                (a,b) for (a,b) in directions
                if a == 0 or b == 0
                ]
        if not allow_reverse:
            directions = [
                (a,b) for (a,b) in directions
                if not (a < 0 or b < 0)
                ]

        data = self.data
        max_row = len(data)
        max_col = len(data[0])
        for i, row in enumerate(data):
            for j, c in enumerate(row):
                if c not in dictionary: continue
                for inc_i, inc_j in directions:
                    d = dictionary
                    i2, j2, c2 = i, j, c
                    so_far = []
                    while True:
                        if len(so_far) >= min_length and self.SENTINEL in d:
                            yield ''.join(so_far), (i, j, inc_i, inc_j)
                        if not (0 <= i2 < max_row and 0 <= j2 < max_col):
                            break
                        c2 = data[i2][j2]
                        so_far.append(c2)
                        if c2 in d:
                            d = d[c2]
                        else:
                            break
                        i2 += inc_i
                        j2 += inc_j

if __name__ == "__main__":
    from sys import argv, exit
    import os
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(
        usage="Usage: %prog [options] puzzle.txt",
        )
    parser.add_option("-d", "--dictionary",
        help="Specify an alternate dictionary (one word per line)",
        action="store",
        dest="dictionary",
        default="/usr/share/dict/words",
        )
    search_options = OptionGroup(parser, "Search options")
    search_options.add_option("--no-diagonals",
        help="Disallow diagonals",
        action="store_false",
        dest="allow_diagonals",
        default=True,
        )
    search_options.add_option("--no-reverse", "--no-backwards",
        help="Disallow reverse matches",
        action="store_false",
        dest="allow_reverse",
        default=True,
        )
    search_options.add_option("-l", "--min-length",
        action="store",
        type="int",
        dest="min_length",
        metavar="LENGTH",
        help="Set the minimum length of interest (default=%i)" %
            DEFAULT_MIN_LENGTH,
        default=DEFAULT_MIN_LENGTH,
        )
    parser.add_option_group(search_options)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        exit(1)
    fname = args[0]
    puzzle = Puzzle(Puzzle.parse_file(fname))
    dictionary = os.path.expanduser(options.dictionary)
    for answer in puzzle.find_words(
            Puzzle.build_dictionary(dictionary),
            allow_reverse=options.allow_reverse,
            allow_diagonals=options.allow_diagonals,
            min_length=options.min_length
            ):
        word, (row, col, dir_row, dir_col) = answer
        direction = Puzzle.dir_to_desc(dir_row, dir_col)
        print("%s at row %i, col %i going %s" % (
            word, 
            row + 1,
            col + 1,
            direction
            ))
