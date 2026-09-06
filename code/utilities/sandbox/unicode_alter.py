# 代码借鉴自：https://www.cnblogs.com/mumuhhh/p/17811377.html

from unicodedata import normalize
from string import ascii_lowercase, digits
from collections import defaultdict
import random

lst = list(ascii_lowercase + digits)
dic = defaultdict(list)
for char in lst:
    for i in range(0x110000):
        if normalize("NFKC", chr(i)) == char:
            dic[char].append(chr(i))
        if len(dic[char]) > 9:
            break

# print(dic)

code = input()
for c in code:
    if not c in dic:
        print(c, end='')
        continue
    if c in digits:
        print(dic[c][8], end='')
        continue
    print(dic[c][1:][0], end='')
    
