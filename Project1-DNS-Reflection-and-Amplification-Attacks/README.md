# Project 1: DNS Reflection and Amplification Attacks

##  raw socket

**non-raw socket** : 在 application 傳輸資料的過程中, 會需要經由一層層 layer 包裝 packet, 包含加上 source ip address, destination ip address等; 而在接收端, 我們收到 packet 之後要將 packet 的 header 給拆掉並根據 protocal 往上傳遞給各層後最後將 data 傳給 application。

如下圖 non-raw socket 可以繞過 OSI model 將 package 送到 application 中, 因此可以實現 sniffer, IP Spoofing Packets 等功能

<div>
    <img src="img/packet.png" width="550" height="200">
    <img src="img/raw.png" width="300">
</div>

## check

* [ ] 要提供 makefile 且命名為 **dns_attack**
* [ ] 確保可以在乾淨 VM 下執行(不可以有依賴其他 Library )
* [ ] Report 字數
* [ ] Report 檔名為: report.pdf 
* [ ] Report 字體: Times New
Roman
* [ ] Report font-size: 11 Or 12

## source

* [stackoverflow : what is RAW socket in socket programming](https://stackoverflow.com/questions/14774668/what-is-raw-socket-in-socket-programming)
* [A Guide to Using Raw Sockets](https://www.opensourceforu.com/2015/03/a-guide-to-using-raw-sockets/)