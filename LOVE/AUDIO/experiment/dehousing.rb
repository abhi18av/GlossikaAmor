
all_files = Dir['*']

# to keep only folders 
folders = all_files.reject {|f| File.file? f}



for fldr in folders
	current_folder = Dir.pwd + '/' + fldr
	files = Dir.entries(current_folder)
	for fl in files
		current_file = current_folder + '/' + fl
		system('mv',current_file, Dir.pwd)
	end
end
