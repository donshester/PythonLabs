import constants


def operation_function(num_1, num_2, operation):
    if operation == constants.ADD:
        return num_1 + num_2

    elif operation == constants.SUB:
        return num_1 - num_2

    elif operation == constants.MUL:
        return num_1 * num_2

    elif operation == constants.DIV:
        return num_1 / num_2

    else:
        return 'Incorrect operation'
