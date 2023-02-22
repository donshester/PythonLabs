import random

print('Hello world!')

def operation_function(num_1, num_2, operation):
    if operation == 'add':
        return num_1+num_2

    elif operation == 'sub':
        return num_1-num_2

    elif operation == 'mul':
        return num_1*num_2

    elif operation == 'div':
        return num_1/num_2
    
    else: 
        return 'Incorrect operation'    

random_list= []

print('Ten random numbers:')

for i in range (10):

    random_number = random.randint(1,100)
    random_list.append(random_number)

    print('{}'.format(random_number), end=' ')

print('\nEven numbers: ')
for num in random_list:
    if num % 2 == 0:
        print(num, end=' ')
    else: 
        continue

