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
    value 3 in {2 4}
    mutation {
        chance 0.6
        step 4
    }
}
gene attack ccc { cost 10 }

dna ddd {bbb vision}
dna eee {aaa dna ddd ccc}

behavior ggg

entity {
    coexistence false
    repr hhh
    at {(1 3) (4 5)}
}

organism {
    dna ddd
    behavior ggg
    repr iii
    at {(6 14) (9 9) (5 0)}
}

organism {
    dna eee
    behavior ggg
    repr jjj
    at {(15 15)}
}

world {
    size {
        width 20
        height 20
    }
    terrain {
        default sand
        dirt
        grass
        water
    }
}

simulation {
    episodes 10
    max_rounds 10
    actions_time 10
    available_commands {}
    stop simulation {
        return false;
    }
}
'''

program = parser.parse(data, lexer=lexer)
print(program)

program.evaluate(context)
