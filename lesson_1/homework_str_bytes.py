# №1
print('\n' + '№1', '-' * 100 + '\n')

unicode_words = []
words = ['разработка', 'сокет', 'декоратор']
for word in words:
    print(type(word), word)
    unicode_words.append(word.encode('unicode_escape'))

for unicode_word in unicode_words:
    print(type(unicode_word), unicode_word)

print('\n' + '№2', '-' * 100 + '\n')

# №2
words = ['class', 'function', 'method']
for word in words:
    byte_word = bytes(word, encoding='utf-8')
    print('type:', type(byte_word), 'contains:', byte_word, 'length:', len(byte_word))

print('\n' + '№3', '-' * 100 + '\n')

# №3
words = ['attribute', 'класс', 'функция', 'type']
for word in words:
    try:
        byte_word = bytes(word, encoding='ascii')
    except UnicodeEncodeError:
        print(word)

print('\n' + '№4', '-' * 100 + '\n')

# №4
words = ['разработка', 'администрирование', 'protocol', 'standard']
for word in words:
    byte_word = word.encode('utf-8')
    print(byte_word)
    str_word = byte_word.decode('utf-8')
    print(str_word)

print('\n' + '№5', '-' * 100 + '\n')

# №5
import subprocess
import chardet

# ARGS = ['ping', 'yandex.ru']
# ARGS = ['ping', 'youtube.com']
# YA_PING = subprocess.Popen(ARGS, stdout=subprocess.PIPE)
# for line in YA_PING.stdout:
#     result = chardet.detect(line)
#     line = line.decode(result['encoding']).encode('utf-8')
#     print(line.decode('utf-8'))

print('\n' + '№6', '-' * 100 + '\n')

# №6
words = ['сетевое программирование\n', 'сокет\n', 'декоратор\n']
with open('test_file.txt', 'w') as file:
    file.writelines(words)

with open('test_file.txt', 'r', encoding='utf-8') as file:
    try:
        print(file.read())
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
