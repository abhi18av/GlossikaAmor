import json


with open("./love_RU_accent.json", encoding="utf-8") as f:
	contents = json.load(f)


d = {}



ACCENT = u'\u0301'
for k,v in contents.items():
	#print(k, " => ", v)
	d[k] = v.replace(ACCENT, "")

#for item in sorted(d.iteritems(), key=lambda x: x[0]):
#    print(item)

with open('love_RU.json', 'w', encoding = "utf-8") as outfile:  
    json.dump(d, outfile, indent = 4, ensure_ascii = False, sort_keys = True)