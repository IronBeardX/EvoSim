# importing required modules
import argparse
from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context

def join_string_list(text_list):
    text = ''
    for line in text_list:
        text += line
    return text

# create a parser object
parser = argparse.ArgumentParser(description="An evolution simulator")

parser.add_argument("path", nargs=1, metavar="path",
                    type=str, help="The path of the evo script.")

parser.add_argument('-d', '--debug', action="store_true", help='Enable debugging')

# parse the arguments from standard input
args = parser.parse_args()

path = args.path[0]

debug = args.debug
lexer = get_lexer(debug=debug)
parser = get_parser(debug=debug, start="program")
context = Context(debug=debug)

# Open file in path and read all text
with open(path) as file:
    code = join_string_list(file.readlines())
    program = parser.parse(code, lexer = lexer)
    program.evaluate(context)

