# Project II: MITM and Pharming Attacks in Wi-Fi Networks

## mitm_attack

* Print out the IP/MAC addresses of all the Wi-Fi devices or VMs except for Attacker and AP/Host

* Print out the username and password which a user submits to the website https://e3.nycu.edu.tw/login/index.php using any of the Wi-Fi devices or VMs



## pharm_attack

* Print out the IP/MAC addresses of all the Wi-Fi devices or VMs except for Attacker and AP/Host

* Redirect the NYCU home page (www.nycu.edu.tw) to the phishing page (140.113.207.246)


## show IP/MAC address

此次作業中兩者首要之務皆為要求先 print 所有與 AP 連線的裝置的 IP/MAC address, 所給的 HINT 為可以使用: **‘scapy’ and ‘netifaces’ library in Python** or **commands ‘nmap’,‘arp’, and ‘route’**

這邊選擇使用 nmap, 先確定我們可以透過:

```
$ sudo nmap -sn 192.168.1.0/24
```

獲得所有目前相同網段的裝置 ip 與 ip address, **注意只有在 sudo 權限下才能夠顯示出 MAC address**, 可以參考 [stackoverflow : is it possible to get the MAC address for machine using nmap](https://stackoverflow.com/questions/13212187/is-it-possible-to-get-the-mac-address-for-machine-using-nmap)中:

> sudo is important. Without sudo, you won't get the MAC address output line

然而