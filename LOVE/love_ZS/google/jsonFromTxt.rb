require 'json'

files = Dir['*.txt']

fileIDAndSentences = Hash.new()



def cleanString(a_str)

x = a_str
x.strip!
y = x.gsub("\n", " ")

return y
end


for f in files

fileID = f.split('.')[0]
sntc = File.read(f)
sentence = cleanString(sntc)
fileIDAndSentences[fileID] =  sentence

end


 File.open('./fileIDAndSentences.json', 'w') do |f|
   f.write(JSON.pretty_generate(fileIDAndSentences))
 end