fp = open("/home/csc2021/materials/victim.dat","r")

victim_data = []
lines = fp.readlines()

for line in lines:
    victim_data.append(str(line.strip()))

if __name__=="__main__":
    print(victim_data)
