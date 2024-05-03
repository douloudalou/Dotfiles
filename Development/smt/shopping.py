class_of_gundam = [
    '1',
    '2',
    '3',
    '4',
    '5',
    'h: home'
]

details = [
    [
        {
            'no': '1',
            'id': '1',
            'name': 'smt',
            'price': '$120'
        },
        {
            'no': '2',
            'id': '2',
            'name': 'meee',
            'price': '23'
        },  
        'h: home'
    ],
    [
        {
            'no': '1',
            'id': '3',
            'name': 'smt2',
            'price': '$1231412'
        },
        {
            'no': '2',
            'id': '4',
            'name': 'MEEE',
            'price': '$12'
        },
        'h: home'
    ]
]

cart = []

smt = [
    '1: remove items',
    '2: change amount of items',
    '3: bill',
    'h: home'
]

home = [
    '1: shopping cart',
    '2: store',
]

def checkHome(choice):
    if choice == 'h':
        main()

def removeItem():
    choice = input('Which item do you want to remove (TYPE THE ID OF THE ITEM): ')
    checkHome(choice)
    for i in cart:
        if cart[i]['id'] == choice:
            cart.pop(cart[i])
        else:
            print('INVALID ID')
            removeItem()

def updateAmount():
    choice = input('Which item do you want to change the amount (TYPE THE ID OF THE ITEM): ')
    checkHome(choice)
    for i in cart:
        if cart[i]['id'] == choice:
            amount = int(input(f'Current: {cart[i]["amount"]}, how many do you want: '))
            cart[i]['amount'] = amount
        else:
            print('INVALID ID')
            updateAmount()


# def bill():

def shopping_cart():
    print(cart, '\n')
    print(smt)
    choice = input('What do you want to do: ')
    checkHome(choice)
    match choice:
        case '1':
            removeItem()
        case '2':
            updateAmount()
        # case '3':
        #     bill()

def gundam_details(index):
    print(details[index])
    choice = int(input('Which do you want to buy: ')) - 1
    checkHome(choice)
    no_of_choice = int(input('How many do you want: '))
    item = details[index][choice]
    item['amount'] = no_of_choice
    del item['no']
    cart.append(item)
    choice = input('Do you want to continue shopping [y/n]: ')
    if choice == 'y':
        store()
    elif choice == 'n':
        main()

def store():
    print(class_of_gundam)
    choice = int(input('Which class of gundam do you want to see: ')) - 1
    checkHome(choice)
    gundam_details(choice)

def nxt(choice):
    if choice == 1:
        shopping_cart()
    elif choice == 2:
        store()

def main():
    print(home)
    choice = int(input('Choose: '))
    nxt(choice)

if __name__ == "__main__":
    main()