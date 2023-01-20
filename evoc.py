# importing required modules
import argparse

def join_string_list(text_list):
    text = ''
    for line in text_list:
        text += line
    return text

# create a parser object
parser = argparse.ArgumentParser(description="An evolution simulator")

parser.add_argument("path", nargs=1, metavar="path",
                    type=str, help="The path of the evo script.")

# parse the arguments from standard input
args = parser.parse_args()

path = args.path[0]

# Open file in path and read all text
with open(path) as file:
    text = join_string_list(file.readlines())
    print(text)

