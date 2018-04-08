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

def split_sentences(raw, lang):
    """
    unsplit - A path to a Europarl XML file with unsplit sentences
    lang    - The 2-character language code of the text's language
    Returns a string of text (with newlines) of the split sentences
    """
    #print("Called split_sentences")
    with open(raw, "r", encoding="utf-8") as r:
        splitting = subprocess.Popen(["./split-sentences.perl", "-l", lang], stdin = r, stdout=subprocess.PIPE, universal_newlines=True)
        split = splitting.communicate()[0] 
        status = splitting.wait()
        if status:
           raise RuntimeError("Sentence splitting script failed with error code %d" % status)
        return str(split)

def de_xml(xml_text):
   """
   xml_text - An array of byte strings with XML (and blank strings) to be cleaned"
   """
   cleaned_text = []
   for line in xml_text.splitlines():
       if line and not(line.startswith("<")): cleaned_text.append(line)
   return cleaned_text       

def main(langs, source_root, cleaned=working_directory()):
    lang = langs[0]
    source_dir = os.path.join(source_root, lang)
    entries = os.listdir(source_dir)
    entries.sort(key = date_tuple)


    cleaned_text = []
    for entry in entries:
        split_text = split_sentences( os.path.join(source_dir, entry), "en")
        cleaned_text += de_xml(split_text)

    with open("output.txt", "w", encoding="utf-8") as w:
        w.write( "\n".join(cleaned_text) )

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args.langs, args.source, args.cleaned)
