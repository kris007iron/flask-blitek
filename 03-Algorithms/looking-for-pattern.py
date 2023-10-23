import re
texts = 'This is a example of looking for pattern in text.'
patterns = 'example'
match = re.search(patterns, texts)
s = match.start()
e = match.end()
print('Found "{}"\nin "{}"\nfrom {} to {} ("{}")'.format(
    match.re.pattern, match.string, s, e, texts[s:e]))
# Found "example"


def knuth_morris_pratt(text, pattern):
    """Yields all starting positions of copies of the pattern in the text.
    Calling conventions are similar to string. Find, but its arguments can be
    lists or iterators, not just strings, it returns all matches, not just
    the first one, and it does not need the whole text in memory at once.
    Whenever it yields, it will have read the text exactly up to and including
    the match that caused the yield."""
    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos - shift]:
            shift += shifts[pos - shift]
        shifts[pos + 1] = shift

    # do the actual search
    start_pos = 0
    match_len = 0
    for c in text:
        while match_len == len(pattern) or \
              match_len >= 0 and pattern[match_len] != c:
            start_pos += shifts[match_len]
            match_len -= shifts[match_len]
        match_len += 1
        if match_len == len(pattern):
            yield start_pos


# now use it
for match in knuth_morris_pratt('This is a example of looking for pattern in text.', 'example'):
    print(match)


def reverse_polish_notation(expression):
    """Evaluate a reverse polish notation expression"""
    # prevent from dividing by 0
    if '/ 0' in expression:
        return 'Division by zero is not allowed'
    stack = []
    for val in expression.split():
        if val in '+-*/':
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = eval('{}{}{}'.format(arg1, val, arg2))
            stack.append(result)
        else:
            stack.append(int(val))
    return stack.pop()


print(reverse_polish_notation('1 2 + 4 / 0'))
# 15
