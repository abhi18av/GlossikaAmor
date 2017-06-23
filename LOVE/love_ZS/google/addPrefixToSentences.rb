

contents = File.read("./joinAllTXT.txt")


sentencesAll = contents.split("\n\n")[0..99]


def cleanPinyin(s)

	len = s.length
	x = s.delete(s[0])
	#puts s[len-1]
	y = x.delete(s[len-1])
	return y

end



for x in sentencesAll

	s = x.split("\n")[1]
	puts cleanPinyin(s)

#puts s

end 