
# Project3

* victim VM
    * ```cat``` 功能依然要正常可以使用, 且 size 不變
    * /home/csc2021/Pictures 裡面所有 **.jpg** (只需要 .jpg ) 需要以 RSA 加密過
    * 一旦執行```cat```, 勒索視窗需要 pop up

* task 2
	* 目前需要使用 cat 來把壓縮檔接在 infected.sh 後面
		* 或許把這步驟放在 server 上執行, 或使用其他方法
	* 還沒處理 size 的部份
	* test.py 內容還沒寫
	* 不清楚如何在最後加上指定 byte (0xdeadbeaf)
