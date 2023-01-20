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
dna ddd {bbb vision}
dna eee {aaa dna ddd ccc}
'''

stmts = parser.parse(data, lexer=lexer)
print(stmts)

context.set_var('gene', {})
context.set_var('dna', {})
for node in stmts:
    node.evaluate(context)

print(context.variables)
