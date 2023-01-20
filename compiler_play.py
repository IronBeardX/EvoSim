from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True, start="test")
context = Context(debug=True)

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

behavior fff {
    func fffa = x y {
        return x + y;
    }
    func fffb = {
        if 1 == 0 {
            return false;
        }
    }
    decide organism time {
        return [3, 'hello'];
    }
}
behavior ggg {
    decide organism time {
        loop x = 1, x < 10, x = x + 1 {
            return;
        }
    }
}

entity {
    coexistence false repr hhh
    at {(1 3) (4 5) (0 100)}
}

organism {
    dna ddd behavior ggg repr iii at {(6 171) (9 90) (46 0)}
}
'''

stmts = parser.parse(data, lexer=lexer)
print(stmts)

context.set_var('gene', {})
context.set_var('dna', {})
context.set_var('behaviors', {})
context.set_var("ent_facts", [])
for node in stmts:
    node.evaluate(context)

print(context.variables)
print(context.children)
