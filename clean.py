import argparse
import os
import subprocess
import re

DEBUG = False

#Functions to help with argument parsing
def working_directory():
    return os.path.abspath(".")

def existing_dir(path):
    absolute = os.path.abspath(path)
    if not os.path.isdir(absolute):
        raise FileNotFoundError("%s is not a directory." % absolute)
    return absolute



def create_parser():
    parser = argparse.ArgumentParser(description="Multi-align Europarl corpora")

    parser.add_argument("--source", required=True, metavar="<path>", type=existing_dir, help="Directory with directories for individual languages (en, es, fr, etc.)")

    parser.add_argument("--cleaned", default=working_directory(), metavar="<path>", type=os.path.abspath, help="Directory to write cleaned corpora")

    parser.add_argument("--langs", required=True, nargs="+", metavar="xx", help="One or more languages in their 2-char ISO abbreviations")

    return parser

def date_tuple(entry):
    start_index = entry.index("ep-") + len("ep-")
    end_index = entry.index(".txt")

    nums = [int(entry) for entry in entry[start_index:end_index].split("-")]
    nums[0] += 1900 if nums[0] > 90 else 2000
    return tuple( nums )

def get_input():
    return input("Enter a Europarl filename: ")

def main(langs, source_root):

    #if len(langs) < 2:
        #raise ValueError("Must specifiy at least two languages")

    initial_dir = os.path.join(source_root, langs[0])
    entries = os.listdir(initial_dir)
    entries.sort(key = date_tuple)
    for entry in entries:
        print(entry)
    #query = get_input()
    #while query:
        #print( date_tuple(query) )
        #query = get_input()

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args.langs, args.source)
