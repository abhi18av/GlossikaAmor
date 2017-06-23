files = Dir['*-C-[0-9][0-9][0-9][0-9].mp3']

Dir.mkdir("C-file")

folder = "./C-file/" 
files.each do |f|
	system('mv', f,folder)
end