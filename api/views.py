from django.shortcuts import render

# Create your views here.
#index the lines in all our subtitles once upon deploy
directory = "../data"
index = 0
sets = {}
for filename in os.listdir(directory):
	subfile = open("../data/"+filename)

	fset = fuzzyset.FuzzySet()

	count = -1
	for line in subfile:
		count += 1

		line = line.strip()
		if count <= 1:
			continue
		elif line == "":
			count = -1
			continue

		fset.add(line)

		index += 1

	sets[filename] = fset
	

def fuzzy_search(query):
	for file in sets:
		res = sets[file].get(query)
		print(res)