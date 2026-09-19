import argparse
import sys


def message(marker, text):
    color = {'-': 31, '+': 32, '~': 33}[marker]
    stream = sys.stdout if marker == '+' else sys.stderr
    print(f'\033[{color}m[{marker}]\033[0m {text}', file=stream, flush=True)


class Parser(argparse.ArgumentParser):
    def error(self, text):
        message('-', text)
        self.exit(2)
