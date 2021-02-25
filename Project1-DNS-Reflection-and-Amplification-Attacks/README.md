# Project 1: DNS Reflection and Amplification Attacks

## socket

socket 可以讓不同 process 或是不同機器間進行通訊, 更精確的說法是可以讓任何使用 **standard Unix file descriptors** 的裝置進行通訊(ps. 我們知道在 linux 之下所有東西都是file, 因此所有 IO action 都是用讀寫 file descriptors 完成的, 實際上它只是一個 integer 而已, 詳細內容可以參考[Linux 的 file descriptor 筆記](https://kkc.github.io/2020/08/22/file-descriptor/)以及[What are file descriptors, explained in simple terms?](https://stackoverflow.com/questions/5256599/what-are-file-descriptors-explained-in-simple-terms)

## raw socket

### non-raw socket : 

在 application 傳輸資料的過程中, 會需要經由一層層 layer 包裝 packet, 包含加上 source ip address, destination ip address等; 而在接收端, 我們收到 packet 之後要將 packet 的 header 給拆掉並根據 protocal 往上傳遞給各層後最後將 data 傳給 application。

如下圖 non-raw socket 可以繞過 OSI model 將 package 送到 application 中, 因此可以實現 sniffer, IP Spoofing Packets 等功能

<div>
    <img src="img/packet.png" width="550" height="200">
    <img src="img/raw.png" width="300">
</div>

### open a raw socket

如果要 open socket 必須要知道三個參數:
1. socket family
2. socket type
3. protocol

然而 raw socket 的 socket family 為 ```AF_PACKET```, socket type 為 ```SOCK_RAW ```, 所以 raw socket is created by calling the ```socket``` syscall :

```c
raw_socket = socket(AF_INET, SOCK_RAW, int protocol);
```

各項詳細說明可以看[這份文件](https://sock-raw.org/papers/sock_raw), [這份文件](https://man7.org/linux/man-pages/man7/raw.7.html), [以及這份文件](https://linux.die.net/man/7/raw), 下面僅會列出部份內容:

<details>
    <summary><b>sock_type</b> click to expand</summary>

>Linux defines these constants in /usr/src/linux-2.6.*/include/linux/socket.h
>
>/* Supported address families. */
#define AF_UNSPEC	0
#define AF_UNIX		1	/* Unix domain sockets 		*/
#define AF_LOCAL	1	/* POSIX name for AF_UNIX	*/
#define AF_INET		2	/* Internet IP Protocol 	*/
>
>/* Protocol families, same as address families. */
#define PF_UNSPEC	AF_UNSPEC
#define PF_UNIX		AF_UNIX
#define PF_LOCAL	AF_LOCAL
#define PF_INET		AF_INET
</details>

<details>
    <summary><b>sock_type</b> click to expand</summary>

>Linux defines the internet family protocol types in 
>/usr/src/linux-2.6.*/include/linux/net.h
>
>enum sock_type {
	SOCK_STREAM	= 1,
	SOCK_DGRAM	= 2,
	SOCK_RAW	= 3,
	SOCK_RDM	= 4,
	SOCK_SEQPACKET	= 5,
	SOCK_DCCP	= 6,
	SOCK_PACKET	= 10,
};
</details>

<details>
    <summary><b>protocol</b> click to expand</summary>

>Linux defines these protocols in /usr/src/linux-2.6.*/include/linux/in.h
>
>/* Standard well-defined IP protocols.  */
enum {
	IPPROTO_IP = 0,			/* Dummy protocol for TCP		*/
	IPPROTO_ICMP = 1,		/* Internet Control Message Protocol	*/
	IPPROTO_IGMP = 2,		/* Internet Group Management Protocol	*/
	IPPROTO_IPIP = 4,		/* IPIP tunnels (older KA9Q tunnels use 94) */
	IPPROTO_TCP = 6,		/* Transmission Control Protocol	*/
	IPPROTO_EGP = 8,		/* Exterior Gateway Protocol		*/
	IPPROTO_PUP = 12,		/* PUP protocol				*/
	IPPROTO_UDP = 17,		/* User Datagram Protocol		*/
	IPPROTO_IDP = 22,		/* XNS IDP protocol			*/
	IPPROTO_DCCP = 33,		/* Datagram Congestion Control Protocol */
	IPPROTO_RSVP = 46,		/* RSVP protocol			*/
	IPPROTO_GRE = 47,		/* Cisco GRE tunnels (rfc 1701,1702)	*/
	IPPROTO_IPV6 = 41,		/* IPv6-in-IPv4 tunnelling		*/
	IPPROTO_ESP = 50,       	/* Encapsulation Security Payload protocol */
	IPPROTO_AH = 51,             	/* Authentication Header protocol       */
	IPPROTO_BEETPH = 94,	       	/* IP option pseudo header for BEET */
	IPPROTO_PIM    = 103,		/* Protocol Independent Multicast	*/
	IPPROTO_COMP   = 108,           /* Compression Header protocol */
	IPPROTO_SCTP   = 132,		/* Stream Control Transport Protocol	*/
	IPPROTO_UDPLITE = 136,		/* UDP-Lite (RFC 3828)			*/
	IPPROTO_RAW	 = 255,		/* Raw IP packets			*/
	IPPROTO_MAX
};

</details>

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