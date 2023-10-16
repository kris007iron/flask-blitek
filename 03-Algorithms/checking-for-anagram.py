def anagram_recursion(s1, s2):
    # recursion
    if len(s1) != len(s2):
        return False
    if len(s1) == 1:
        return s1 == s2
    if s1[0] in s2:
        return anagram_recursion(s1[1:], s2.replace(s1[0], '', 1))
    return False


def anagram_iteration(s1, s2):
    # iteration
    if len(s1) != len(s2):
        return False
    for i in s1:
        if i in s2:
            s2 = s2.replace(i, '', 1)
    return s2 == ''


word1 = input("Enter the first word: ")
word2 = input("Enter the second word: ")
print(anagram_recursion(word1, word2))
print(anagram_iteration(word1, word2))
