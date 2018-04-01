import argparse
import os

DEBUG = True

def working_directory():
    return os.path.abspath(".")

def existing_dir(path):
    absolute = os.path.abspath(path)
    if not os.path.isdir(absolute):
        raise FileNotFoundError("%s is not a directory." % absolute)
    return absolute

def entries_as_set(directory):
    return {entry for entry in os.listdir(directory)}

def create_parser():
    parser = argparse.ArgumentParser(description="Multi-align Europarl corpora")

    parser.add_argument("--source", required=True, metavar="<path>", type=existing_dir, help="Directory with directories for individual languages (en, es, fr, etc.)")

    parser.add_argument("--aligned", default=working_directory(), metavar="<path>", type=os.path.abspath, help="Directory to write aligned corpora")


    parser.add_argument("--langs", required=True, nargs="+", metavar="xx", help="Two or more languages in their 2-char ISO abbreviations")

    return parser

def main(source_root, aligned_root, langs):
    source_root = existing_dir(source_root)
    aligned_root = os.path.abspath(aligned_root)

    if len(langs) < 2:
        raise ValueError("Must specifiy at least two languages")

    source_dirs = []
    aligned_dirs = []

    for lang in langs:
       source_dir = existing_dir(os.path.join(source_root, lang))
       aligned_dir = os.path.join(aligned_root, lang)
       if not os.path.exists(aligned_dir): os.makedirs(aligned_dir)
       source_dirs.append(source_dir)
       aligned_dirs.append(aligned_dir)

    intersection = entries_as_set(source_dirs[0])
    for source_dir in source_dirs[1:]:
        intersection = intersection & entries_as_set(source_dir)

    if DEBUG:
        for i in range(len(langs)):
            trimmed = sorted( list(entries_as_set(source_dirs[i]) - intersection) )
            print("Entries trimmed from %s" % langs[i])
            for entry in trimmed: print(entry)

    for i in range(len(langs)):
        source_dir = source_dirs[i]
        aligned_dir = aligned_dirs[i]

        for entry in intersection:
            orig_entry = os.path.join(source_dir, entry)
            link_entry = os.path.join(aligned_dir, entry)
            os.symlink(orig_entry, link_entry)


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args.source, args.aligned, args.langs) 
