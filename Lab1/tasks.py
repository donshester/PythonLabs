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

