from operations import operation_function
from random import randint


print('Hello world!')


random_list= []

print('Ten random numbers:')

for i in range (10):

    random_number = randint(1,100)
    random_list.append(random_number)

    print('{}'.format(random_number), end=' ')

print('\nEven numbers: ')
for num in random_list:
    if num % 2 == 0:
        print(num, end=' ')
    else: 
        continue
