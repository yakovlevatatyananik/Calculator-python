class rpn:
    def __init__(self):

        self.formula_string = None
        self.parsed_formula = None
        self.polish = None

        self.OPERATORS = {
            '+': (1, lambda x, y: x + y), 
            '-': (1, lambda x, y: x - y),
            '*': (2, lambda x, y: x * y), 
            '/': (2, lambda x, y: x / y),
            '~': (2, lambda x: -x)}

    def parse(self):
        number = ''
        for s in self.formula_string:
            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            elif (s not in '1234567890.') and (s not in self.OPERATORS) and (s not in "()"):
                print('Input error')
                quit()
            if s in self.OPERATORS or s in "()":
                yield s
        if self.formula_string[0] in '+-*/':
            print('Input error')
            quit()
        if number:
            yield float(number)

    def shunting_yard(self):
        stack = []
        for token in self.parsed_formula:
            if token in self.OPERATORS:
                while stack and stack[-1] != "(" and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(self):
        stack = []
        for token in self.polish:
            if token in self.OPERATORS:
                if token == '~':
                    x = stack.pop()
                    stack.append(self.OPERATORS[token][1](x))
                else:
                    y, x = stack.pop(), stack.pop()
                    try:
                        stack.append(self.OPERATORS[token][1](x, y))
                    except (IndexError, ZeroDivisionError):
                        print('Violation of mathematical properties')
                        quit()
            else:
                stack.append(token)
        return stack[0]

    def __call__(self, expression):
        self.formula_string = expression
        self.parsed_formula = self.parse()
        self.polish = self.shunting_yard()
        result = self.calc()
        return result

def main():
    calc = rpn()
    expression = input("> ")
    result = calc(expression)
    print(result)

if __name__ == "__main__":
    main()
