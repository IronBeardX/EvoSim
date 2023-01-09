from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True)

context = Context()
text = '''x = -2
loop i = 0, i < 5, i = i + 1 {
    if not x {
        break
    }
    x = x + 1
}
'''

stmts = parser.parse(text, lexer=lexer)
for node in stmts:
    node.evaluate(context)

print(context.variables)
