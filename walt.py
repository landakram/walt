import random
import sys
import re
from collections import defaultdict

def chunked(seq, size):
    return (tuple(seq[pos:pos + size]) for pos in xrange(0, len(seq), size))

class Walt(object):
    def __init__(self, corpus, order=3):
        self.order = order + 1
        self.db = defaultdict(list)
        self.corpus = list()
        self.train(corpus)

    def train(self, corpus):
        corpus = corpus.strip().lower()
        corpus = re.sub('\r', '', corpus)
        corpus = re.sub(' +',' ', corpus)
        corpus = re.sub('\n+', '\n', corpus)
        c = corpus.splitlines(True)
        for line in c:
            self.corpus += line.strip().split()
            self.corpus[-1] += '\n'

        for chunk in chunked(self.corpus, self.order):
            self.db[chunk[:-1]].append(chunk[-1])

    def random_chain(self):
        i = random.randint(0, len(self.corpus) - self.order)
        return self.corpus[i : (i + self.order - 1)]

    def compose(self, number_of_lines):
        result = list()
        chain = self.random_chain()
        next_word = None

        current_line_number = 1
        first = True
        while current_line_number < number_of_lines:
            w = chain[0].lower()

            if first:
                w = w.capitalize()
                first = False
            if w == 'i':
                w = w.capitalize()

            if w.endswith('\n'):
                current_line_number += 1
                first = True

            result.append(w)

            choices = self.db[tuple(chain)]
            while len(choices) == 0:
                chain = self.random_chain()
                choices = self.db[tuple(chain)]
            next_word = random.choice(choices)

            chain = chain[1:]
            chain.append(next_word)

        result += chain
        r = ' '.join(result)
        return re.sub('\n ', '\n', r)

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        walt = Walt(f.read(), order=2)
    print walt.compose(int(sys.argv[2]))
