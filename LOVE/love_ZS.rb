require 'json'


source_lang = "zh-TW"
target_lang = "zh-CN"

engine = "google"
engineStr = " -engine=" + engine


f = File.read("./love-ZT.json")
fileHash = JSON.parse(f)

sentences = []

fileHash.each do |k,v|



sentencesQ = sentences.map{ |e| %{"#{e}'"} }


len = sentencesQ.length - 1


for i in (0..len).to_a
	cmd1 = "trans " + source_lang + ":" + target_lang + " " + sentencesQ[i-1] + ' -no-ansi ' + engineStr
	print(cmd1)
	fileName = (i+1).to_s + ".txt"
	cmd2 = cmd1 + " > " + fileName
	#system(cmd2)
	puts(cmd2)
end



#str.sub("*\e[22m*", "X")


# using concurrent-ruby gem from this point on


#gem install concurrent-ruby
