try:
    open('./f0/f0.restart.xsc', 'r').readlines()
    directions = {'BACKWARD': 50, 'FORWARD': 50}
except FileNotFoundError:
    directions = {'BACKWARD': 16}
    test = True

for key, val in directions.items():
    for i in range(val):
        c = key[0].lower()
        lines = [line.strip() for line in open(f'{c}{i}/{c}{i}.restart.xsc').readlines()]
        steps = lines[2].split()[0]
        if test:
            print(f'{key} {i}: {steps}/550000')
        elif steps != '550000':
            print(f'{key} {i}: {steps}/550000')
