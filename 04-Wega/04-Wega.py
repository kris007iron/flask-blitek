print(''.join([open('przyklad.txt').readlines()[i][9] for i in range(39, len(open('przyklad.txt').readlines()), 40)]))
lines = open('przyklad.txt').readlines()
max_unique_letters = 0
for i in lines:
    unique_letters = len(set(i))
    if unique_letters > max_unique_letters:
        max_unique_letters = unique_letters

print(max_unique_letters)
