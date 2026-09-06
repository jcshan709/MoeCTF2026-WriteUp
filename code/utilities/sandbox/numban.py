s = input("")
out1 = ''
out2 = ''
for c in s:
    out1 += f'chr(len("{'a'*ord(c)}"))+'
print(out1[:-1])
