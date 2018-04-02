import argparse
import os
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

    parser.add_argument("--train", default=working_directory(), metavar="<path>", type=os.path.abspath, help="Directory to write aligned corpora")

    parser.add_argument("--test", default=None, metavar="<path>", type=os.path.abspath, help="Directory to write aligned test corpora from year 2000, Q4")


    parser.add_argument("--langs", required=True, nargs="+", metavar="xx", help="Two or more languages in their 2-char ISO abbreviations")

    return parser

#Utility functions for script
def entries_as_set(directory):
    return {entry for entry in os.listdir(directory)}

def make_links(entries, source_dir, dest_dir):
     for entry in entries:
        orig_entry = os.path.join(source_dir, entry)
        link_entry = os.path.join(dest_dir, entry)
        os.symlink(orig_entry, link_entry)

def main(langs, source_root, train_root, test_root=None):
    source_root = existing_dir(source_root)
    train_root = os.path.abspath(train_root)
    test_root = os.path.abspath(test_root) if test_root else None

    if len(langs) < 2:
        raise ValueError("Must specifiy at least two languages")

    source_dirs = []
    train_dirs = []
    if test_root: test_dirs = []

    for lang in langs:
       source_dir = existing_dir(os.path.join(source_root, lang))
       source_dirs.append(source_dir)

       train_dir = os.path.join(train_root, lang)
       if not os.path.exists(train_dir): os.makedirs(train_dir)
       train_dirs.append(train_dir)

       if test_root:
           test_dir = os.path.join(test_root, lang)
           if not os.path.exists(test_dir): os.makedirs(test_dir)
           test_dirs.append(test_dir)

    intersection = entries_as_set(source_dirs[0])
    for source_dir in source_dirs[1:]:
        intersection = intersection & entries_as_set(source_dir)

    if test_root:
        #Pattern matching all files from the fourth quarter of the year 2000
        pattern = re.compile( "ep-00-1[012]\\S*")
        q4_2000 = []
        for entry in intersection:
            if pattern.match(entry): q4_2000.append(entry)
        test_intersection = set(q4_2000)
        train_intersection = intersection - test_intersection
    else:
        train_intersection = intersection

    if DEBUG:
        for i in range(len(langs)):
            trimmed = sorted( list(entries_as_set(source_dirs[i]) - intersection) )
            print("Entries trimmed from %s" % langs[i])
            for entry in trimmed: print(entry)

    for i in range(len(langs)):
        source_dir = source_dirs[i]
        train_dir = train_dirs[i]

        make_links(train_intersection, source_dir, train_dir)
        if test_root:
            test_dir = test_dirs[i]
            make_links(test_intersection, source_dir, test_dir)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args.langs, args.source, args.train, args.test)
