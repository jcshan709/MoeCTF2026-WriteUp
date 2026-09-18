# backdoor - WriteUp  
> 本题知识点：  
> - 常用 pwn 工具 `checksec` 的使用
> - 反编译二进制文件  
> - python `pwnlib` 的使用  
> - 基本的 `ret2text` 型攻击  

## *checksec* 的使用  
`checksec`是一个linux下的ELF安全检测工具，可以显示`NX` `PIE`等安全信息。  
本题仅涉及到了`PIE`，故仅对`PIE`作简单讲解  
### PIE(ASLR)  
地址空间配置随机加载（Address Space Layout Randomization，ASLR）是一种防范内存损坏漏洞被利用的计算机安全技术。ASLR通过随机放置进程关键数据区域的地址空间来防止攻击者能可靠地跳转到内存的特定位置来利用函数。现代操作系统一般都加设这一机制。  
  
PIE 是 gcc 编译器的功能选项，作用于程序（ELF）编译过程中。是一个针对代码段（ .text ）、数据段（ .data ）、未初始化全局变量段（ .bss ）等固定地址的一个防护技术，如果程序开启了PIE保护的话，在每次加载程序时都变换加载地址。  


