import sys
import os
import argparse
import subprocess

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

    parser.add_argument("--verbose", "-v", action="store_true", help="Display progress messages")

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
        splitting = subprocess.Popen(["./split-sentences.perl", "-l", lang], stdin = r, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
        split = splitting.communicate()[0] 
        status = splitting.wait()
        if status:
           raise RuntimeError("Sentence splitting script failed with error code %d" % status)
        return str(split)

def de_xml(xml_text):
   """
   xml_text - An array of strings with XML and blank strings to be cleaned"
   """
   cleaned_text = []
   for line in xml_text.splitlines():
       if line and not(line.startswith("<")): cleaned_text.append(line)
   return cleaned_text       

def align(xml_texts):
    indices = [0 for i in range(len(xml_texts))]
    print(indices)


def content_remaining(entries, indices):
    for i in range(len(entries)):
       if indices[i] >= len(entries[i]): return False
    return True

def sentence_align(entries):
    
    indices = [0 for i in range(len(entries))] #One index to scroll through each language's entry

    aligned_entries = [ [] for i in range(len(entries)) ]

    next_xml = [ "" for i range(len(entries)) ]

    while content_remaining(entries, indices):

        
    

def alt_main(langs, source_root, cleaned_root=working_directory, verbose=False):
    if not os.path.exists(cleaned_root): os.makedirs(cleaned_root)
    entries = os.listdir(os.path.join(source_root, langs[0])) #The entries need only be computed once
    entries.sort(key = date_tuple)

    #List of dimensions ( len(entries), len(langs) )
    #Each element of split_corpora is another list, whose entries are string representations for the entry in each lang
    split_corpora = []
    for entry in entries:
        parallel_entries = [split_sentences(os.path.join(source_root, lang, entry), "en") for lang in langs]
        split_corpora.append( parallel_entries )

    #i = 1
    #for entry in split_corpora[0]:
       #print("ENTRY %d" % i)
       #print(entry)
       #i += 1

    first_doc = split_corpora[0]

def main(langs, source_root, cleaned_root=working_directory(), verbose=False):

    if not os.path.exists(cleaned_root): os.makedirs(cleaned_root)
    entries = os.listdir(os.path.join(source_root, langs[0])) #The entries need only be computed once
    entries.sort(key = date_tuple)

    split_corpora = []
    for lang in langs:
        source_dir = os.path.join(source_root, lang)

        split_corpus = []
        for entry in entries:
            split_corpus += split_sentences( os.path.join(source_dir, entry), "en").splitlines()

        split_corpora.append( split_corpus )
    

    align(split_corpora)


    """
    cleaned_corpus = os.path.join(cleaned_root, lang + ".txt")
    with open(cleaned_corpus, "w", encoding="utf-8") as w:
        w.write( "\n".join(cleaned_text) )
    if verbose: print("Wrote cleaned corpus %s" % cleaned_corpus, file=sys.stderr)
    """ 


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    alt_main(args.langs, args.source, args.cleaned, verbose=args.verbose)
