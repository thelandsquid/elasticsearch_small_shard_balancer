from scripts.ShardGrowth import ShardGrowth
from scripts.SmallShardSimulation import Small_Shard_Simulation
from scripts.LargestIndices import LargestIndicesScript
from config.FileSizeDict import FileSizeDict

def user_commands():
    scripts = [LargestIndicesScript, ShardGrowth, Small_Shard_Simulation]
    
    print('----------------------------------------')
    print('    ELASTICSEARCH ASSISTANCE SCRIPTS    ')
    print('----------------------------------------')

    while(True):
        print('Select script by number: ')
        for i in range(len(scripts)):
            print('['+str(i+1)+']',scripts[i].get_script_name())
        print('[0] EXIT PROGRAM')

        choice = input()
        if not choice.isdigit():
            print('CHOICE MUST BE A NUMERICAL VALUE')
            continue
        choice = int(choice)

        if choice==0:
            exit(0)
        else:
            required_args = scripts[choice-1].get_required_args()
            args_list = []
            for (var_name, default, desc) in required_args:
                print("Set \""+var_name+"\" --- "+desc+"  ["+str(default)+"]")
                user_input = input()
                if user_input=='':
                    user_input = default
                args_list.append(user_input)
            scripts[choice-1](*args_list)
            print('\n\n')