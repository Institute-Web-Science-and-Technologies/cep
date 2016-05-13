#!/bin/bash

export INPUT_FILE=$1
export OUTPUT_DIR=$2
export FORMAT=$3

for SCRIPT in ./*.py
do
	echo "executing ${SCRIPT}"
	python $SCRIPT "${INPUT_FILE}" "${OUTPUT_DIR}" "${FORMAT}"
done
