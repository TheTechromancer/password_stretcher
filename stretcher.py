#!/usr/bin/env python3

'''

by TheTechromancer

'''

from time import sleep
from lib.utils import *
from pathlib import Path
from lib.mangler import *
from statistics import mean
from functools import reduce
from os import name as os_type
from sys import argv, exit, stdin, stderr, stdout
from argparse import ArgumentParser, FileType, ArgumentError




def stretcher(options):

    show_written_count = not stdout.isatty()
    written_count = 0

    mangler = Mangler(
        in_list=options.wordlist,
        double=options.double,
        perm=options.permutations,
        leet=options.leet,
        cap=options.cap,
        capswap=options.capswap,
    )

    estimated_output_size = (mangler.average_word_size+1) * len(mangler)
    stderr.write(f'[+] Estimated output: {len(mangler):,} words ({bytes_to_human(estimated_output_size)})\n')
    sleep(2)

    for mangled_word in mangler:

        stdout.buffer.write(mangled_word + b'\n')
        if show_written_count and written_count % 1000 == 0:
            stderr.write('\r[+] {:,} words written'.format(written_count))

        written_count += 1

    if show_written_count:
        stderr.write('\r[+] {:,} words written\n'.format(written_count))

    stdout.buffer.flush()
    stdout.close()



if __name__ == '__main__':

    ### ARGUMENTS ###

    parser = ArgumentParser(description="FETCH THE PASSWORD STRETCHER")

    parser.add_argument('-r',       '--wordlist',       type=ReadFile,    default=ReadSTDIN(),      help="wordlist to analyze / stretch (default: STDIN)", metavar='')
    parser.add_argument('-L',       '--leet',           action='store_true',                        help="\"leetspeak\" mutations")
    parser.add_argument('-c',       '--cap',            action='store_true',                        help="common upper/lowercase variations")
    parser.add_argument('-C',       '--capswap',        action='store_true',                        help="all possible case combinations")
    parser.add_argument('-dd',      '--double',         action='store_true',                        help="double each word (e.g. \"Pass\" --> \"PassPass\")")
    parser.add_argument('-P',       '--permutations',   type=int,               default=1,          help="Max permutation depth (careful! massive output)", metavar='INT')


    try:

        options = parser.parse_args()

        # print help if there's nothing to analyze
        if type(options.wordlist) == ReadSTDIN and stdin.isatty():
            parser.print_help()
            stderr.write('\n\n[!] Please specify wordlist or pipe to STDIN\n')
            exit(2)

        stretcher(options)


    except ArgumentError:
        stderr.write("\n[!] Check your syntax. Use -h for help.\n")
        exit(2)
    except AssertionError as e:
        stderr.write("\n[!] {}\n".format(str(e)))
        exit(1)
    except (BrokenPipeError, IOError):
        pass
    except KeyboardInterrupt:
        stderr.write("\n[!] Program interrupted.\n")
        exit(2)