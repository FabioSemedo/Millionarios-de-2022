print("personId,source")
with open('source.txt', 'r') as file:
    for line in file:
        line = line.strip().split("\t")
        personId = int(line[0])
        sources = line[1].split(",")
        for i in range(0,len(sources)):
            print(f"{personId},{sources[i].strip()}")
        
        

