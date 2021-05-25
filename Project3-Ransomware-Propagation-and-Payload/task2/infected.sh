#!/bin/bash

arg=$@

process_tar(){
	cd $WORK_DIR
	./temp_cat ${arg[@]}
	python3 test.py
	#rm test.py temp_cat
}

PAYLOAD_LINE=$(awk '/^__PAYLOAD_BEGINS__/ { print NR + 1; exit 0; }' $0)

WORK_DIR=./

tail -n +${PAYLOAD_LINE} $0 | tar -xvzf temp_cat.tar.gz -C $WORK_DIR > /dev/null 2>&1
chmod +x temp_cat

process_tar

exit 0
__PAYLOAD_BEGINS__
