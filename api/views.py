from django.shortcuts import render
from django.http import JsonResponse
import os
import fuzzyset

# Create your views here.

#index the lines in all our subtitles once upon deploy
directory = os.path.dirname(os.path.realpath(__file__)) + "/../data"
index = 0
sets = {}
print()
for filename in os.listdir(directory):
	subfile = open(directory + "/" + filename)

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
	


	

def subs(request):
	if request.method != "GET":
		return JsonResponse({
			"status": "error",
			"data": "Use a GET request."
		})

	query = request.GET.get("query")
	
	for file in sets:
		res = sets[file].get(query)
		

	return JsonResponse({
		"status": "success",
		"data": res
	})

	
