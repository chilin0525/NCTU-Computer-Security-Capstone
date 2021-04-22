# Project II: MITM and Pharming Attacks in Wi-Fi Networks

## mitm_attack

* Print out the IP/MAC addresses of all the Wi-Fi devices or VMs except for Attacker and AP/Host

* Print out the username and password which a user submits to the website https://e3.nycu.edu.tw/login/index.php using any of the Wi-Fi devices or VMs


### show IP/MAC address

此次作業中兩者首要之務皆為要求先 print 所有與 AP 連線的裝置的 IP/MAC address, 所給的 HINT 為可以使用: **‘scapy’ and ‘netifaces’ library in Python** or **commands ‘nmap’,‘arp’, and ‘route’**

這邊實做選擇使用 nmap, 先確定我們可以透過:

```
$ sudo nmap -sn 192.168.1.0/24
```

獲得所有目前相同網段的裝置 ip 與 ip address, **注意只有在 sudo 權限下才能夠顯示出 MAC address**, 可以參考 [stackoverflow : is it possible to get the MAC address for machine using nmap](https://stackoverflow.com/questions/13212187/is-it-possible-to-get-the-mac-address-for-machine-using-nmap)中:

> sudo is important. Without sudo, you won't get the MAC address output line

Step:
1. 透過 socket connection, 得知目前使用的 ip address
2. 透過 ```ip addr``` 可以得知目前所有網卡資訊, 因為 nmap 需要知道 subnet mask, 我們用 regular expression 去抓取 ip addr 中含有 ip/subnet mask 的所有資訊, 例如(10.1.10.1/24, 192.168.1.1/27, etc), 並用步驟一獲得的 ip 進行比對就可以獲得 ip + subnet mask 資訊, 之後使用 nmap 就可以直接這組資訊
3. 透過 ```ip route``` 獲得目前所使用的網卡是哪張, 同時也可以獲得 default gatewat 的資訊
4. 將步驟三的網卡名稱丟入 ```getMAC(NIC_name)``` 即可獲得 Host 的 MAC address, 截至目前為止我們可以獲得 Host ip, MAC address
5. 透過 ```get_default_gateway_linux()``` 獲取 default gateway 的 ip
6. 利用 nmap 的結果利用 Regular expression 擷取出所有 ip 與 MAC, 因為 nmap 掃不出 host 本身的 MAC, 因此 IP 的結果會比 MAC 還要多出一組數據, 因此後續需要先過濾 Host IP 讓 IP 與 MAC 的陣列長度相等, 否則後須會有 index error 發生
7. 擷取出 gateway 的 ip 與 MAC address, 並且從 ip 與 MAC 陣列中移出去, 之後做攻擊時 ip 與 MAC 就是包含所有 victim 的陣列

### packet forwarding

在上面設定完而且開啟 linux 的 ip forwarding 功能後:

```
$ echo 1 > /proc/sys/net/ipv4/ip_forward
```

上面重開啟後會被 reset 為0, 使用下面指令將直接永遠開啟讓 device 有 router 的功能, 擇一即可

```
$ sysctl -w net.ipv4.ip_forward=1
```


### sslsplit

* install:

    ```
    $ sudo apt-get update -y
    $ sudo apt-get install -y sslsplit
    ```

---

## pharming attack

* NetfilterQueue:

    * install:
        * **does not support Python3.6+**, last release is 2017 = =
        * ```pip3 install NetfilterQueue```
    * API:
        * [NetfilterQueue 0.8.1](https://pypi.org/project/NetfilterQueue/)


## report link : https://docs.google.com/document/d/1UMfpEAWTXPlP57mHasa24kYqOxnc_tftqwv1ILeY5Hk/edit
