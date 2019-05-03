with open('Demofile.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

plate="RTZ043"
data[0] = plate+'\n'

with open('Demofile.txt', 'w') as file:
    file.writelines( data )