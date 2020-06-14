numbers = ""
variable_info = {}
stack = []
stack1 = []
top = -1


# for evaluation process
def precedence_order(item):
    if item == '^':
        return 3
    elif item == '*' or item == '/':
        return 2
    elif item == '+' or item == '-':
        return 1
    else:
        return -1


def precedence_check(item):
    try:
        if precedence_order(item) <= precedence_order(stack[len(stack) - 1]):
            return True
        else:
            return False
    except (KeyError, IndexError):
        return False


def push(element):
    global top
    top += 1
    stack.append(element)


def pop():
    global top
    top -= 1
    return stack.pop()


def peek():
    return stack[len(stack) - 1]


def is_empty():
    return True if len(stack) == 0 else False


def evaluator_main(expression):
    try:
        postfix = []
        for i in expression.split():
            if i.isdigit() or i.isalpha():
                postfix.append(i)
            elif i == " ":
                continue
            elif i == "(":
                push(i)
            elif i == ")":
                while peek() != "(":
                    postfix.append(pop())
                if peek() == "(":
                    postfix.append(pop())
            else:
                while precedence_check(i):
                    postfix.append(pop())
                push(i)
        while not is_empty():
            postfix.append(pop())
        for i in postfix:
            if i.isdigit() or i.isalpha():
                push(i)
            else:
                if i == '+':
                    val1 = int(pop())
                    val2 = int(pop())
                    push(val2 + val1)
                elif i == '-':
                    val1 = int(pop())
                    val2 = int(pop())
                    push(val2 - val1)
                elif i == '*':
                    val1 = int(pop())
                    val2 = int(pop())
                    push(val2 * val1)
                elif i == '/':
                    val1 = int(pop())
                    val2 = int(pop())
                    push(val2 / val1)
                elif i == '^':
                    val1 = int(pop())
                    val2 = int(pop())
                    push(val2 ** val1)
        return stack.pop()
    except:
        if ValueError:
            print("Unknown variable")
        elif IndexError:
            print("Invalid expression (error code 3)")


# evaluation process end


# for extracting multi-digits numbers and making spaces
def maker(expression):
    resultant = []
    temp = ''
    expression += "X"
    for i in expression:
        flag = 0
        if i.isdigit():
            flag = 1
        if flag == 1:
            temp += i
        if flag == 0:
            resultant.append(temp)
            temp = ''
        if i == "+" or i == "-" or i == "*" or i == "/" or i == "(" or i == ")" or i == "^" or i.isalpha():
            resultant.append(i)
    new_string = ""
    i = 0
    while resultant[i] != "X":
        new_string += resultant[i] + " "
        i += 1
    return new_string


# for checking parenthesis in string
def parenthesis_check(expression):
    try:
        for i in expression:
            if i == '(' or i == '{' or i == '[':
                stack1.append(i)
            elif i == ')' or i == '}' or i == ']':
                if not balance_check(i):
                    return False
        return True if len(stack1) == 0 else False
    except IndexError:
        return False


def balance_check(close):
    x = stack1.pop()
    if x == '(' and close == ')':
        return True
    elif x == '{' and close == '}':
        return True
    elif x == '[' and close == ']':
        return True
    else:
        return False


def correction_evaluation(string):
    try:
        expression = []
        for i in string.split():
            if i.startswith("+") and i.endswith("+"):
                expression.append("+")
            elif i.startswith("-") and i.endswith("-"):
                if i.count("-") % 2 == 0:
                    expression.append("+")
                else:
                    expression.append("-")
            elif (i == "*" and len(i) > 1) or (i == "/" and len(i) > 1):
                print("Invalid expression (error code 2)")
            elif i in variable_info.keys():
                expression.append(variable_info[i])
            else:
                expression.append(i)
        return " ".join(expression)
    except KeyError:
        print("Unknown variable")


def storing_variable(assignment):
    try:
        assignment = assignment.split("=")
        if any(i.isdigit() for i in assignment[0]):
            print("Invalid identifier")
            main_()
        else:
            for i in range(1, len(assignment) - 1):
                if any(j.isdigit() for j in assignment[i]):
                    print("Invalid assignment")
                    main_()
            if any(j.isdigit() for j in assignment[len(assignment) - 1].strip()):
                if assignment[len(assignment) - 1].strip() not in variable_info.keys() and not any(
                        j.isdigit() for j in assignment[len(assignment) - 1].strip()):
                    print("Unknown variable")
                    main_()
                elif assignment[len(assignment) - 1].strip() in variable_info.keys():
                    x = 1
                elif assignment[len(assignment) - 1].strip().isdigit():
                    x = 0
                else:
                    print("Invalid assignment")
                    main_()
        for i in range(len(assignment) - 1):
            if assignment[len(assignment) - 1].strip().isdigit():
                variable_info[assignment[i].strip()] = assignment[len(assignment) - 1].strip()
            else:
                variable_info[assignment[i].strip()] = variable_info[assignment[len(assignment) - 1].strip()]
    except KeyError:
        print("Unknown variable")


def fetch(variable):
    try:
        if variable in variable_info.keys():
            return variable_info[variable]
        else:
            return "Unknown variable"
    except KeyError:
        print("Unknown variable")


def main_():
    global numbers
    while True:
        numbers = input()
        if numbers == "":
            continue
        elif numbers == "/help":
            print("The program calculates the sum of numbers")
            print("If you enter '--' the it will become a '+' i.e. two adjacent minus signs turn into a plus.")
        elif numbers == "/exit":
            print("Bye!")
            exit(0)
        elif numbers.startswith("/"):
            print("Unknown command")
        elif "=" in numbers:
            storing_variable(numbers)
        elif (
                "+" in numbers or
                "-" in numbers or
                "*" in numbers or
                "/" in numbers or
                "^" in numbers
        ) and len(numbers) > 2:
            if not parenthesis_check(numbers):
                print("Invalid expression (error code 4)")
                main_()
            numbers = correction_evaluation(numbers)
            numbers = maker(numbers)
            numbers = correction_evaluation(numbers)
            x = evaluator_main(numbers)
            if x is not None:
                print(x)
            else:
                continue
        else:
            if numbers.endswith("-"):
                print("Invalid expression (error code 1)")
                main_()
            print(fetch(numbers))


main_()
