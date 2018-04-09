import sys
import os
import argparse
import subprocess
import re

DEBUG = True

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


#Global regular expression for extracting the ID attribute from an XML tag
ID_PATTERN = re.compile(r"ID=(\d+)")
def tag_id(tag):
    return int( ID_PATTERN.search(tag).group(1) )

def content_remaining(entry_set, indices):
    for i in range(len(entry_set)):
       if indices[i] >= len(entry_set[i]): return False
    return True

def chapter_tag(line):
    return line.startswith("<CHAPTER")

def common_chapter(entry_set, indices):
    last_id = tag_id( entry_set[0][ indices[0] ] )
    for i in range(1, len(entry_set)):
        current_id = tag_id( entry_set[i][ indices[i] ] )
        if current_id != last_id: return False
    return True

def next_chapter(lines, i):
    i += 1
    while (i < len(lines)) and not(chapter_tag(lines[i])): i += 1
    return i

def next_common_chapter(entry_set, indices):
    """
    indices -- Original indices
    """
    indices = [i + 1 for i in indices] #Increment, because we're looking for the *next* chapter

    i = 0
    while content_remaining(entry_set, indices) and (i < len(entry_set)):
        if not chapter_tag( entry_set[i][ indices[i] ] ):
            indices[i] = next_chapter( entry_set[i], indices[i] )
        i += 1

    if DEBUG and not content_remaining(entry_set, indices):
        print("next_common_chapter: no content remaining")
        return indices 

    chapter_ids = [ tag_id( entry_set[i][ indices[i] ] ) for i in range(len(entry_set)) ]
    max_id = max(chapter_ids)

    while content_remaining(entry_set, indices) and not( common_chapter(entry_set, indices) ):
        i = 0
        while i < len(entry_set) and not(common_chapter(entry_set, indices)):
            if chapter_ids[i] < max_id:
                indices[i] = next_chapter(entry_set[i], indices[i])
                chapter_ids[i] = tag_id( entry_set[i][ indices[i] ] )
                if chapter_ids[i] > max_id: max_id = chapter_ids[i]
            i += 1

    if DEBUG and not content_remaining(entry_set, indices):
        print("next_common_chapter: no content remaining")

    return indices

def chapter_align(entry_set):
    """
    entry_set - A list of strings, each of which is the entry for a given language
    """

    
    indices = [0 for i in range(len(entry_set))] #One index to scroll through each language's entry

    aligned_content = [ [] for i in range(len(entry_set)) ]

    if not common_chapter(entry_set, indices): indices = next_common_chapter(entry_set, indices)
    while content_remaining(entry_set, indices):
        for i in range(len(entry_set)):
            entry = entry_set[i]
            j = indices[i] + 1
            while j < len(entry) and not(chapter_tag(entry[j])):
                aligned_content[i].append( entry[j] )
                j += 1
            indices[i] = j
        if content_remaining(entry_set, indices) and not common_chapter(entry_set, indices):
            indices = next_common_chapter(entry_set, indices)

    print(indices)
    return aligned_content
    

def alt_main(langs, source_root, cleaned_root=working_directory, verbose=False):
    if not os.path.exists(cleaned_root): os.makedirs(cleaned_root)
    entries = os.listdir(os.path.join(source_root, langs[0])) #The file path basenames need only be computed once
    entries.sort(key = date_tuple)

    #List of dimensions ( len(entries), len(langs), varies )
    #Each element of split_corpora is another list, each of whose entries is, again, a list of strings
    split_corpora = []
    for entry in entries:
        parallel_entries = [split_sentences(os.path.join(source_root, lang, entry), "en").splitlines() for lang in langs]
        split_corpora.append( parallel_entries )

    first_doc = split_corpora[0]
    #print(first_doc)

    first_chapter_aligned = chapter_align(first_doc)
    #lengths = [ len(entry) for entry in first_chapter_aligned ]
    #print(lengths)
    i = 1
    for entry in first_chapter_aligned:
        print("LANG %d" % i)
        for line in entry: print(line)

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
