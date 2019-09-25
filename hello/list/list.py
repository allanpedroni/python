def main():
    list = [3, 22, 5.3, 20]

    # deleting item from list
    # list.remove(1)
    # del list[0]
    list.pop(0)

    # inserting new itens in list
    list.append(33)
    # list.append("teste")

    # length of list
    print(f'Total itens List: {len(list):d}')

    print(f'Max item: {max(list):d}')

    # numbers = [2, 5, 7, 9]
    # print(min(numbers))

    print(f'Min item: {min(list)}')

    list.reverse()
    print('Reserve list:', list)

    list.sort(reverse=False)
    print(list)

    for elem in list[:]:
        # elem = elem + 1
        print(f"elem bef {elem} after {elem + 1}", )

    list_of_squares = [int ** 2 for int in range(1, 10)]

    print('New list of squares: {}'.format(list_of_squares))


# before python 3
# if '__main__' == __name__:
#    remove_item_from_list(1)
# print(list)

main()
