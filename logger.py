import os

# the results are logged after every game finishes

def logger(details: dict, winner):

    file = logNamer()

    open(file, 'w')

    for npc in details.items():
        npc = str(npc)


        with open(file, 'a') as _file:


            currentnpc = npc[2:9].strip()

            if currentnpc.endswith("'"):
                index = currentnpc.index("'")
                currentnpc = currentnpc[0:index]
            if currentnpc.endswith(","):
                index = currentnpc.index(",")
                currentnpc = currentnpc[0:index-1]

            if currentnpc == winner:
                _file.write(f'WINNER: {npc}\n')
            else:
                _file.write(f'{npc}\n')


def logNamer():
    path = 'logs\\'

    filecount = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    filename = filecount + 1

    logfile = 'log' + str(filename) + '.txt'
    file = path + logfile

    return file
