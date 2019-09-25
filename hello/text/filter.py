"""
Check if given string's length is 2
"""


def isOfLengthFour(strObj):
    if len(strObj) == 2:
        return True
    else:
        return False


def main():
    # List of string
    listOfStr = ['hi', 'this', 'is', 'a', 'very', 'simple', 'string', 'for', 'us']

    print('Original List : ', listOfStr)

    print('*** Filter list using filter() and a function ***')

    filteredList = list(filter(isOfLengthFour, listOfStr))

    print('Filtered List : ', filteredList)

    print('*** Filter list using filter() and a Lambda Function ***')

    filteredList = list(filter(lambda x: len(x) == 2, listOfStr))

    print('Filtered List : ', filteredList)

    print('*** Filter characters from a string using filter() ***')

    strObj = 'Hi this is a sample string, a very sample string'

    filteredChars = ''.join((filter(lambda x: x not in ['a', 's'], strObj)))

    print('Filtered Characters  : ', filteredChars)

    print('*** Filter an array in Python using filter() ***')

    array1 = [1, 3, 4, 5, 21, 33, 45, 66, 77, 88, 99, 5, 3, 32, 55, 66, 77, 22, 3, 4, 5]

    array2 = [5, 3, 66]

    filteredArray = list(filter(lambda x: x not in array2, array1))

    print('Filtered Array  : ', filteredArray)

    # source: https://www.computerhope.com/issues/ch001721.htm
    # Find string in text - USING FIND
    given_text = 'Poderiam por favor avaliar o Pull Request 0212 abaixo, referente a api de usuário do SSO Santander.'
    given_text = given_text + 'Inclusão da camada de 1232 infra.'
    given_text = given_text + 'Pull Request 1832 '

    print('PR found:', given_text.find('1832'))

    # source: https://www.computerhope.com/issues/ch001721.htm
    # https://www.w3schools.com/python/python_regex.asp
    # https://www.guru99.com/python-regular-expressions-complete-tutorial.html
    # Incorporating regular expressions
    import re

    pat = re.compile(r"(g\d{4})", re.IGNORECASE)

    founds = re.findall(r'\d{4}', given_text, re.MULTILINE)
        # re.findall(r"(g\d{4})",given_text)
        # pat.findall(given_text)

    print(''.join(e + ',' for e in founds))

    for f in founds:
        print(f)

    # print('found value:',found.groups())

    if founds is not None:
        print('fount it')
    else:
        print('not')


main()
