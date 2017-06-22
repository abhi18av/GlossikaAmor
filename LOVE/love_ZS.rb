require 'json'
require 'shellwords'

f = File.read("./love_ZT.json")

source_lang = "zh-TW"
target_lang = "zh-CN"

engine = "google"
engineStr = " -engine=" + engine


contents = JSON.parse(f)

sentences = []

contents.each do |k,v|

sentences.push(v)
end

sentencesQ = sentences.map{ |e| %{"#{e}"} }


len = sentencesQ.length - 1


for i in (0..len).to_a
	cmd1 = "trans " + source_lang + ":" + target_lang + " " + sentencesQ[i-1] + ' -no-ansi ' + engineStr
	puts(cmd1)
	#system(cmd1)

	#fileName = (i+1).to_s + ".txt"
	#cmd2 = cmd1 + " > " + fileName
	#system(cmd2)
	#puts(cmd2)
end



