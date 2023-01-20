from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True, start="test_world")

context = Context()
text = '''
world {
    size infinite { width 1920 height 1080 }
    terrain {
        aaa
        default bbb
        ccc at {1 2 3}
        ddd
        eee at {4 5}
        fff
    }
}
'''

expr = parser.parse(text, lexer=lexer)

print(expr)
