#!/bin/bash

LANGS=(da de en es fi fr it nl pt sv)
NUM_LANGS=${#LANGS[@]}

TRAIN=""
TEST="TRUE"

typeset -i i j
for (( i=8; i<$NUM_LANGS; ++i ))
do 
  for (( j=0; j<$NUM_LANGS; ++j ))
  do
    if [ $i != $j ]
    then
        if [ $TRAIN ]
        then
            echo "Generated training corpora for ${LANGS[$i]}-->${LANGS[$j]} at" `date`
        fi

        if [ $TEST ]
        then
            ./gen_parallel.sh "test" ${LANGS[$i]} ${LANGS[$j]} "test_clean" "test"
            echo "Generated test corpora for ${LANGS[$i]}-->${LANGS[$j]} at" `date`
        fi
    fi
  done
done
