import rushin
import json


with open("./love_RU_accent.json") as f:
	contents = json.load(f)


d = {}




for k,v in contents.items():
	#print(k, " => ", v)
	d[k] = rushin.strip_text(v, include_stress = False)



with open('out.json', 'w') as outfile:  
    json.dump(d, outfile)