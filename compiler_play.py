from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True, start="test")
context = Context()

data = '''
gene vision
gene health aaa {
    value 5 in {0 10}
    mutation {
        chance 0.5
        step 1
    }
}
gene fins bbb {
    value 3 in {2 4} mutation {
        chance 0.6 step 4
    }
}
gene attack ccc { cost 10 }
'''

context.set_var('gene', {})

stmts = parser.parse(data, lexer=lexer)
for node in stmts:
    node.evaluate(context)

print(context.variables)
