#!/bin/bash

SRC_LANG=$1
DST_LANG=$2

RAW_DIR=$3
PROCESSED_DIR=$4

SRC_ENTRIES=`ls $RAW_DIR/$SRC_LANG/`
DST_ENTRIES=`ls $RAW_DIR/$DST_LANG/`

for SRC_ENTRY in $SRC_ENTRIES
do
  cat $RAW_DIR/$SRC_LANG/$SRC_ENTRY | \
      ./split-sentences.perl -l $SRC_LANG | \
      ./tokenizer.perl -l $SRC_LANG \
      > $PROCESSED_DIR/$SRC_ENTRY
done

