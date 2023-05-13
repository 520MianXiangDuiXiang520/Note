import ply.lex as lex
import ply.yacc as yacc


class MyLexer:

    # reserved = {
    #     'if': 'IF',
    #     'then': 'THEN',
    #     'else': 'ELSE',
    #     'while': 'WHILE',
    # }
    # tokens = ("NUMBER", "CHAR") + tuple(reserved.values())
    tokens = ("NUMBER", "CHAR")
    literals = ['+', '-', '*', '/', '(', ')', '=']
    t_ignore = (" ")

    def __init__(self, **kwargs) -> None:
        self.lexer: lex.Lexer = lex.lex(module=self, **kwargs)

    def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+'
        t.value = int(t.value)
        return t

    def t_CHAR(self, t: lex.LexToken) -> lex.LexToken:
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # t.type = self.reserved.get(t.value, 'CHAR')
        return t

    def t_error(self, t: lex.LexToken) -> lex.LexToken:
        print(f"Illegal character '{t.value}' in {t.lineno}:{t.lexpos}")
        t.lexer.skip(1)

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def p_expression_uminus(self, p):
        '''expression : "-" expression %prec UMINUS'''
        p[0] = -p[2]

    def p_assignment(self, p):
        '''assignment : CHAR "=" expression'''
        p[0] = p[3]

    def p_expression(self, p):
        '''expression : expression "+" expression
                      | expression "-" expression
                      | expression "*" expression
                      | expression "/" expression
                      | "(" expression ")"
                      | NUMBER'''
        if len(p) == 4:
            match p[2]:
                case "+":
                    p[0] = p[1] + p[3]
                case "-":
                    p[0] = p[1] - p[3]
                case "*":
                    p[0] = p[1] * p[3]
                case "/":
                    p[0] = p[1] / p[3]
        elif len(p) == 3:
            p[0] = [2]
        elif len(p) == 2:
            p[0] = p[1]

    def run(self, data):
        self.lexer.input(data)
        self.parser = yacc.yacc(module=self, start="assignment")
        result = self.parser.parse(data)
        print(result)


if __name__ == "__main__":
    data = "a=12+3 * 9 - 5*-3"
    lexer = MyLexer()
    lexer.run(data)
