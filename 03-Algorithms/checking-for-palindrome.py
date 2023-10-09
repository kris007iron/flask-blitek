# check if word is a palindrome
string = input("Enter a word: ")


def is_palindrome(word: str) -> bool:
    return word == word[::-1]


print(is_palindrome(string))
