letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z']
message = input('Enter a message: ').lower()
offset = int(input('Enter an offset: '))
encrypted_message = ''

for letter in message:
    if letter in letters:
        position = letters.index(letter)
        new_position = (position + offset) % len(letters)
        encrypted_message += letters[new_position]
    else:
        encrypted_message += letter

print(encrypted_message)
