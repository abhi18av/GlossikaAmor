files = Dir['*.txt']


contents = []





for f in files.sort

text = File.read(f)

contents.push(text)

end


#puts contents[0]


for i in 0...(contents.length)

puts("\n")
temp = contents[i]
puts temp
puts("\n")
end
