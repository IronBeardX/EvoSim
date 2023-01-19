from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True, start="test")

context = Context()
text = '''
func fib = nth {
    if nth == 1 or nth == 2 {
        return 1
    }
    return fib(nth - 1) + fib(nth - 2)
}
fib(25)
'''

f, expr = parser.parse(text, lexer=lexer)
f.evaluate(context)
v = expr.evaluate(context)

print(v)
