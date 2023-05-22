s = 'hello'
s = s + 'world'
s = s + '♞'
# s = s.encode('utf8')
# s = bytes.decode(s, 'utf8')
# s = bytes.decode(s)
print(s)
# my_bytes = s.encode('utf-8')

text_file = open('test.txt', 'w', encoding='utf-8')
n = text_file.write(s)
text_file.close()
