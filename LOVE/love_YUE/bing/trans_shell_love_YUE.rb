require 'json'
require 'Shellwords'

f = File.read("../../love_ZT/love_ZT.json")

source_lang = "zh-TW"
target_lang = "yue"

engine = "bing"
engineStr = " -engine=" + engine


contents = JSON.parse(f)

sentences = []

contents.each do |k,v|

sentences.push(v)
end

sentencesQ = sentences.map{ |e| %{"#{e}"} }


len = sentencesQ.length - 1

#Dir.mkdir("love_ZS")

contents.each do |k,v|
	cmd1 = "trans " + source_lang + ":" + target_lang + " " + %{"#{v}"} + ' -no-ansi ' + engineStr 
	puts(cmd1)
	#system(cmd1)

	fileName = k.to_s + ".txt"
	#puts(k)
	cmd2 = cmd1 + " > " + fileName
	system(cmd2)
	#puts(cmd2)
end



