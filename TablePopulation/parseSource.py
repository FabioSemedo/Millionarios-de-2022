print("personId,source")
with open('source.txt', 'r') as file:
    for line in file:
        line = line.strip().split("\t")
        personId = int(line[0])
        sources = line[1].split(",")
        
        for i in range(0,len(sources)):
            sources[i] = sources[i].strip()       #Remove whitespaces around string
            if sources[i][0].islower():           #Capitalised first letter
                sources[i] = sources[i][0].upper() + sources[i][1:]
            print(f"{personId},{sources[i]}")
        
        

