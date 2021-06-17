
## 1-fildes

* trace code first:

	```c
	if(!strncmp("YOUSHALLNOTPASS\n", buf, MAX_LEN)){
		printf("Maybe you learn something :)\n");

		system("/bin/cat flag");
		exit(0);
	}
	```

	* 觀察可以知道如果要 print flag, ```strncmp("YOUSHALLNOTPASS\n", buf, MAX_LEN)``` 結果就必須得是 0, 代表 ```buf``` 前 100 長度的內容要與 ```"YOUSHALLNOTPASS\n"```, 一樣
	* 接著再往上分析, ```len = read(fd, buf, MAX_LEN);``` 可以知道說 read 要從 fd 這個 File Descriptor 讀取長度為 MAX_LEN 的內容, 而 fd 又是由下面片段決定, :

		```c
		len = read(0, buf, MAX_LEN);
		fd = atoi( buf ) - 0xDEADBEAF;
		```

		* 綜合上述 fd 將會從 buf - oxDEADBEAF 決定, 而 buf 內容是 STDIN, 也就是我們可以輸入決定的, 因此如果我們也輸入 0xDEADBEAF fd 將會變成 0, 那下面 read 將會變成 ```read(0, buf, MAX_LEN)```, 此時如果又輸入 "YOUSHALLNOTPASS\n" 就可以取得 flag

		* 如果一開始沒有輸入 0xDEADBEAF 且 file decript 不存在那回傳值就會是 -1, 將沒辦法有第二次輸入機會
	
		![](img/DEADBEAF.png)

### ref

* [Linux 系統程式設計 - fd 及 open()、close() 系統呼叫](https://blog.jaycetyle.com/2018/12/linux-fd-open-close/)
* [Linux 系統程式設計 - read()、write() 與 page cache](https://blog.jaycetyle.com/2019/01/linux-read-write/)
* [File I/O and Standard I/O](https://www.kshuang.xyz/doku.php/course:nctu-%E9%AB%98%E7%AD%89unix%E7%A8%8B%E5%BC%8F%E8%A8%AD%E8%A8%88:chapter3)
* [strncmp](http://tw.gitbook.net/c_standard_library/c_function_strncmp.html)
* [atoi](http://tw.gitbook.net/c_standard_library/c_function_atoi.html)

---

## 2-time_will_sleep

* [peda](https://github.com/longld/peda)

## 3-translator

![](img/3-1.png)
![](img/3-2.png)

compare 的內容:

![](img/3-3.png)

再往上:

![](img/3-4.png)

<br>

```c
#include<stdio.h>

int main(){
    printf("%c", (unsigned char)(-186));
    printf("%c",(unsigned char)(-180));
    printf("%c",(unsigned char)(-191));
    printf("%c", (unsigned char)(-185));
}
/*
abs(-186+126=-60)=> chr(60)="<"
abs(-180+126=-54)=> chr(54)="6"
abs(-191+126=-65)=> chr(65)="A"
abs(-185+126=-59)=> chr(59)=";"
*/
```

* [ghidra 官方](https://ghidra-sre.org/)
* [install ghidra](http://www.ylmzcmlttn.com/2019/03/26/ghidra-installation-on-ubuntu-18-04-16-04-14-04/)

---

## 4-teleport

* Buffer overflow: 
	* 發生主要原因: 因為將 data copy 到 buffer 時沒有做檢查導致 source data 比 destionation size 還大

* [緩衝區溢位攻擊之一(Buffer Overflow)](https://medium.com/@ktecv2000/%E7%B7%A9%E8%A1%9D%E5%8D%80%E6%BA%A2%E4%BD%8D%E6%94%BB%E6%93%8A%E4%B9%8B%E4%B8%80-buffer-overflow-83516aa80240)
* [https://stackoverflow.com/questions/47449110/buffer-overflow-exploit-issue](https://stackoverflow.com/questions/47449110/buffer-overflow-exploit-issue)


如果將以下內容當作 input:

```python
import os

sol = "aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnppppqqqqrrrrssss"
sol += "aaaa"   # 0x4011b6

print(sol,end="") 
```

將會得到:

![](img/4.png)

因此只要把 win address 寫入即可

---

## 5-GOT

首先，先觀察一下 source code 中發現 ```vuln``` function 中並沒有 return value, 因此我們不能像前面那題一樣去修改 return value 讓程式重新導向到 ```flag_func``` function 之中, 但可以看到 ```vuln``` function 最後呼叫了 ```exit()```， 因此這邊成為我們可以動手腳的地方。

### GOT

首先得先提到 static link 與 dynamic link, static link 是指 program 會含有所有他們需要的程式碼內容, 不依賴任何外部的 library

The Global Offset Table(GOT),  program 中用來儲存 dynamic linked 的 function address, 在大多數的程式中並不會把所有用到的 function 程式碼放進來, 可以想像我們時常使用到例如 IO 的 function, 如果每份程式都得將 IO 程式碼給儲存起來再經過編譯, disk 中就會出現大量的一樣程式碼, 因此常用的 function(例如 libc 中的) 是只儲存一份在 disk 中當需要使用的時候再 link 到程式中。問題是今天要怎麼知道該 function address 是多少, 而且 address 還會因為  ASLR load libraries 隨機給予 address 防止攻擊, 因此 **relocation** (**resolution**) 這種方法被發展出來, 當 program 呼叫這些 library 中的 function 時, linker 會負責在 runtime 負責找到這些記憶體位址。對於這種 dynamic link 的 function address 是直到 main program 中被 launch 才會載入到 memory 中, 也就是說直到第一次被呼叫該 function 所對應的 address 才會被 resolve, 而一旦經過第一次解析已經知道該 function address 將會被儲存在 GOT 中可以避免下次被呼叫時又需要經過 dynamic resolver

### PLT

Procedure Linkage Table (PLT), 在 function address 被解析之前, GOT 會指向 PLT 中的 entry, 為負責呼叫 dynamic linker 與需要解析的 function name 的 stub function


1. ```.got```: 就是 GOT, global offset table, 負責儲存 linker 所填入的 external symbol 的 offset 的一張表
2. ```.plt```: stubs 負責尋找 .got.plt 中 section 的 address, 負責 jump to right address 或是請 linker 去搜尋 address
3. ```.got.plt```: GOT for PLT, 包含真正的 target address(在他們被搜尋過後)
4. ```.plt.got```:

### sol


![](img/5-1.png)

![](img/5-2.png)

測試時先用 A 看會出現在哪個位置:

```
str = " %p "*100
str += "AAAAAAAA"
print(str)
```

![](img/5-3.png)

利用輸入時輸入常數把 0x404038 寫入 stack, 把 A 換成 0x404038, 再利用 %n 寫入 0x4011b6

利用 format 格式避免字串過長:

```
>>> 0x4011b6-2
4198836
```

### ref

* [CTF-101:GOT](https://ctf101.org/binary-exploitation/what-is-the-got/)
* [GOT and PLT for pwning.](https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html)
* [A simple Format String exploit example - bin 0x11](https://www.youtube.com/watch?v=0WvrSfcdq1I&ab_channel=LiveOverflow)
* [Format String Exploit and overwrite the Global Offset Table - bin 0x13](https://www.youtube.com/watch?v=t1LH9D5cuK4&list=PLhixgUqwRTjxglIswKp9mpkfPNfHkzyeN&index=23&ab_channel=LiveOverflowLiveOverflow%E5%B7%B2%E9%A9%97%E8%AD%89)
* [Adapting the 32bit exploit to 64bit for format4 - bin 0x27](https://www.youtube.com/watch?v=_lO_rwaK_pY&ab_channel=LiveOverflow)
* [Linux/ELF動態鏈接部分機制(GOT&PLT)](https://hackmd.io/@rhythm/ry5pxN6NI)
* [ctf-course](https://github.com/qazbnm456/ctf-course/blob/master/slides/w4/format-string.md)
* [從任意寫入到任意執行-深入淺出 Got Hijacking](https://slide.duckll.tw/2018/hitcon/#/)
* [計算機原理系列之八——– 可執行文件的PLT和GOT](https://luomuxiaoxiao.com/?p=578)

---

## 6-Secret

第四個看起來就是 RSP 但是失敗了, 第三八個看起來也可以行, 雖然與 rbp 差了 0x20 不過到時候多扣即可 (原本扣 0x100 改成扣 0x120)

![](img/6-1.png)

![](img/6-2.png)

![](img/6-3.png)


### ref

* [Python 3 concatenate string with bytes](https://www.reddit.com/r/LiveOverflow/comments/ep6v6b/python_3_concatenate_string_with_bytes/)
* [Python 2 vs 3 for Binary Exploitation Scripts](https://www.youtube.com/watch?v=FxNS-zSS7MQ&ab_channel=LiveOverflow)
* [What is the right way to pack a payload with Python3's pwntools](https://reverseengineering.stackexchange.com/questions/19776/what-is-the-right-way-to-pack-a-payload-with-python3s-pwntools)

---

## x86 Asm

### register

* 8 個 32-bit general purpose registers, 如下圖
	![](img/register.png)
	* register name not case-sensitive, 所以 ```EAX``` 等於 ```eax```
	* last significant 2 byte of ```EAX``` 稱為 AX, 其中又可以將 AX 裡頭再分為 AH 與 AL
	* special purposes 
		* stack pointer (ESP) 
		* base pointer (EBP): aka. frame pointer
* EIP: 下一個 instruction 的 address
* RBP 為 64 bit architectures 的 EBP (see [Allocating variables on the stack in x86 assembly. rbp and rsp vs esp and ebp](https://stackoverflow.com/questions/42488996/allocating-variables-on-the-stack-in-x86-assembly-rbp-and-rsp-vs-esp-and-ebp)), 其他同理

### Memory and Addressing Modes

* Addressing Memory
	* 直接看例子:
		
		```asm
		mov eax, [ebx]			; 將 EBX 所指向的 32 bit memory address 內容 mov 到 EAX
		mov [var], ebx			; 將 EBX 內容 mov 到 var 這個 memory address (var 是 32 bit 常數)
		mov eax, [esi-4]		; 將 ESI + (-4)  memory address 的 4 bytes 內容 mov 到 EAX
		mov [esi+eax], cl		; 將 CL 的內容 mov 到 ESI+EAX
		mov edx, [esi+4*ebx]	; 將 ESI+4*EBX  這個 address 上的資料 mov 到 EDX
		```

	* 不合法:

		```asm
		mov eax, [ebx-ecx]		; Can only add register values
		mov [eax+esi+edi], ebx 	; At most 2 registers in address computation
		```

* Size Directives

	|name|bytes|
	|--|--|
	|BYTE PTR|1|
	|WORD PTR|2|
	|DWORD PTR|4|

	```asm
	mov BYTE PTR [ebx], 2	; Move 2 into the single byte at the address stored in EBX.
	mov WORD PTR [ebx], 2	; Move the 16-bit integer representation of 2 into the 2 bytes starting at the address in EBX.
	mov DWORD PTR [ebx], 2    	; Move the 32-bit integer representation of 2 into the 4 bytes starting at the address in EBX.
	```

* instruction:
	* 要用直接查 [x86 Assembly Guide](http://www.cs.virginia.edu/~evans/cs216/guides/x86.html)

* calling convention:
	* 在寫 ASM 遇到 function 時, 我們知道可以由 caller 或是 callee 進行協調說誰要負責備份當前的 register 資訊, function 結束誰要負責清理, 將 ptr 回歸等等
	* cdecl（C declaration)
		* 

### ref

1. [x86 Assembly Guide](http://www.cs.virginia.edu/~evans/cs216/guides/x86.html)

---

## activation record(stack frame)

### basic

* why need?
	* 用來儲存機器狀態, 例如 program counter, machine registers 等等
	
	![](img/ar.png)

		* 當今天我們沒有 AR 時會發生什麼事, 以上圖為例我們在 ```main``` 裡頭已經寫好 a, b 的值, 接著呼叫 ```foo```, 然後原本的 a, b 值就馬上被覆蓋過去了, 再回到 ```main``` 時進行 a+b 就會有問題, 因此我們需要在 call function 前就先將有用到的東西給備份好
		* 且 local 只會在 function scope 裡面使用
		* 通常 function 需要備份的東西大同小異(機器所需要備份的暫存器), 因此 ARI(activation record instance) 應該會一樣, 當需要用到時 push 到 stack, 不需要時再 pop 掉(非真正清除)

* stack frame 綜合上述就是一塊可以存放 incoming parameters, local variables 等等的記憶體空間, 並且是分配在 process 的 stack 上面
* frame pointer 就是紀錄 function's frame 的起始 address, 根據 function 需求, 如果需要空間來擺設 variable 等等的話就是以 frame pointer 進行 offset 放入該記憶體位置
* stacl pointer 則是會隨著 function 執行 push 或是 pop 時而變動, 而 frame pointer 並不會隨著 function 中 push pop 而變動而是固定指向該 function 起始位置

### function call

* during function call(x86 architectures):
	1. 將目前 frame pointer push 進入 stack (push ```ebp``` or ```rbp```)
	2. 將 stack pointer 指向 frame pointer, 藉此定義了 function start address
	3. 根據 function size 將 stack pointer 減去需要的 memory size(在 x86 架構中 stack 是由 high address 往 low address 生長的)
	4. callee 準備完成, 可以執行 function 中的內容, 通常會用到 frame pointer with negative offset 來取值
	5. function 內都執行完畢, 將 frame pointer 複製到 stack pointer(也就是 callee **清除 stack frame 的動作**, 注意編譯器在清除時並不會真的把資料刪除, 而是只是移動 stack pointer 而已), 最後 pop 出 old frame pointer, aka ```leave``` instruction
	6. 執行 ```ret``` 回到 caller

* [關於 call 與 leave](https://blog.csdn.net/striver1205/article/details/25695437)
* [calling convention](https://sites.google.com/view/28-assembly-language/x86-assembly-%E7%9A%84-stack-frame-%E5%92%8C%E5%87%BD%E6%95%B8%E7%9A%84%E5%91%BC%E5%8F%AB%E6%85%A3%E4%BE%8B)

### ref

* [Stack frames:A really quick explanation of stack frames and frame pointers](https://www.cs.rutgers.edu/~pxk/419/notes/frames.html)
* [x86 Assembly Guide](http://www.cs.virginia.edu/~evans/cs216/guides/x86.html)
* [函數呼叫](https://liquid0118.pixnet.net/blog/post/48494862)
* [C的function call與stack frame心得](https://my.oschina.net/tsh/blog/1613642)