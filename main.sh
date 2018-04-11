#!/bin/bash

RAW=../txt
PROCESSED=intermediary

if [ ! -e $RAW ]
then
  mkdir $RAW
fi

if [ ! -e $PROCESSED ]
then
  mkdir $PROCESSED
fi

./split_and_tokenize.sh es en $RAW $PROCESSED
