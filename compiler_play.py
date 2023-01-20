from src.compiler.lexer import get_lexer
from src.compiler.parser import get_parser
from src.compiler.context import Context


lexer = get_lexer(debug=True)
parser = get_parser(debug=True, start="test")
context = Context(debug=True)

data = '''
entity {
    coexistence false
    repr A
    at {(1 2) (1 3) (1 4)}
}

world {
    size {
        width 20
        height 20
    }
    terrain {
        s
    }
}

simulation {
    episodes 1
    max_rounds 2
    actions_time 1
    available_commands {}
    stop simulation {
        'wrapping necessary functions';

        ents_around_pos = simulation.entities_around_position;
        ents_in_position = simulation.entities_in_position;
        kill = simulation.kill_in_position;
        create = simulation.create_in_position;
        print = simulation.gol_visualizer;


        'implementing the game of life';
        count = 0;
        command_list = [];
        loop i = 0, i < simulation.world.world_map.shape[0], i = i + 1{
            loop j = 0, j < simulation.world.world_map.shape[1], j = j + 1{
                position = [i, j];
                entities_count = ents_around_pos(position);
                current_ent = ents_in_position(position);
                if entities_count < 2{
                    if current_ent > 0{
                        command_list = command_list + [[kill, position]];
                        count = count + 1;
                    }
                }
                else if entities_count > 3{
                    if current_ent > 0{
                        command_list = command_list + [[kill, position]];
                        count = count + 1;
                    }
                }
                if entities_count == 3{
                    if current_ent == 0{
                        command_list = command_list + [[create, position]];
                        count = count + 1;
                    }
                }
            }
        }
        
        loop i = 0, i < count, i = i + 1{
            command = command_list[i][0];
            command(command_list[i][1]);
        }
        print();
        return false;
    }
}
'''

program = parser.parse(data, lexer=lexer)
print(program)

program.evaluate(context)
