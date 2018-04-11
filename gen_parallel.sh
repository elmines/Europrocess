#!/bin/bash

IN_DIR=$1
SRC_LANG=$2
DST_LANG=$3
OUT_DIR=$4/${SRC_LANG}-${DST_LANG}
CORP_NAME=$5

UNALIGNED=unaligned
ALIGNED=aligned
rm -rf $UNALIGNED/* $ALIGNED/*

TOOLS=tools

mkdir -p $UNALIGNED/$SRC_LANG ${UNALIGNED}/$DST_LANG $ALIGNED $OUT_DIR

#Split and Tokenize
spltk() {
  MY_LANG=$1

  ENTRIES=`ls $IN_DIR/$MY_LANG/`
  for ENTRY in $ENTRIES
  do
    cat $IN_DIR/$MY_LANG/$ENTRY | \
        $TOOLS/split-sentences.perl -l $MY_LANG | \
        $TOOLS/tokenizer.perl -l $MY_LANG \
        > $UNALIGNED/$MY_LANG/$ENTRY
  done
}
spltk $SRC_LANG
spltk $DST_LANG

./sentence-align-corpus.perl $SRC_LANG $DST_LANG `pwd`/$UNALIGNED `pwd`/$ALIGNED

ALIGNED_ENTRIES=`ls $ALIGNED/${SRC_LANG}-${DST_LANG}/$SRC_LANG/`

XML_BASENAME=xml
XML_SRC=$XML_BASENAME.$SRC_LANG
XML_DST=$XML_BASENAME.$DST_LANG

OLD_PATH=`pwd`
#echo "My directory is $OLD_PATH"
cd $ALIGNED/${SRC_LANG}-${DST_LANG}/$SRC_LANG/
cat `ls` > ../$XML_SRC

cd $OLD_PATH/$ALIGNED/${SRC_LANG}-${DST_LANG}/$DST_LANG/
cat `ls` > ../$XML_DST
cd $OLD_PATH


$TOOLS/de-xml.perl $ALIGNED/${SRC_LANG}-${DST_LANG}/$XML_BASENAME $SRC_LANG $DST_LANG $OUT_DIR/$CORP_NAME
