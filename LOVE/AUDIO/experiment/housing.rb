files = Dir.glob('*.mp3')

houses = []

files.each do |f|
	a_house = f.split('-')[0]
	houses.push(a_house)
end

require 'set'

rooms = houses.to_set


rooms.each do |r|
   Dir.mkdir(r)
end  


for f in files
	house = f.split('-')[0]
	for r in rooms
		if r == house
			system('mv', f, r)
		end
	end
end
