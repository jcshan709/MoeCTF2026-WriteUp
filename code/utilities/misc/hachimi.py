with open('result.txt') as f:
    s = list(f.read())
    s.insert(618, chr(0x200B))
    open('result.2.txt', 'w').write(''.join(s))
    counter = {}
    for i in map(lambda x: f'U+{hex(ord(x))[2:].upper().rjust(4, "0")}', s):
        counter[i] = counter.setdefault(i, 0) + 1
    for k, v in counter.items():
        print(f'{k}: {v}')