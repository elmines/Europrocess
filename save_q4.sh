#!/bin/bash

SOURCE=txt
LANGS=(da de en es fi fr it nl pt sv)
#LANGS=(en es fi fr it nl pt sv)
#bg  cs  da  de  el  en  es  et  fi  fr  hu  it  lt  lv  nl  pl  pt  ro  sk  sl  sv

#echo ${LANGS[@]}
#exit 0

TRAIN=train
TEST="test"

mkdir -p $TRAIN
mkdir -p $TEST

for LANG in ${LANGS[@]}
do
  mkdir -p $TEST/$LANG
  mkdir -p $TRAIN/$LANG

  cp $SOURCE/$LANG/* $TRAIN/$LANG/

  Q4=`ls $SOURCE/$LANG/ | grep ep-00-1[012]-*`
  #echo $Q4
  for ENTRY in $Q4
  do
    mv $TRAIN/$LANG/$ENTRY $TEST/$LANG/
  done

done
