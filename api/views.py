from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os, mimetypes
import fuzzyset

THRESHOLD = 0.3

# Index the lines in all our subtitles once upon deploy
directory = os.path.dirname(os.path.realpath(__file__)) + "/../data"
index = 0
sets = {}
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
	
	accurate = None
	accurate_file = None
	for file in sets:
		if accurate == None:
			accurate = sets[file].get(query)[0]
			accurate_file = file
		else:
			current = sets[file].get(query)[0]
			current_file = file
			if current[0] > accurate[0]:
				accurate = current
				accurate_file = current_file
	
	if accurate[0] < THRESHOLD:
		return JsonResponse({
			"status": "error",
			"data": {
				"message": "Not conclusive.",
				"result": None,
				"srt": None
			}
		})
	else:
		return JsonResponse({
			"status": "success",
			"data": {
				"message": None,
				"result": accurate,
				"srt": accurate_file
			}
		})

def files(request):
	if request.method != "GET":
		return JsonResponse({
			"status": "error",
			"data": "Use a GET request."
		})

	filename = request.GET.get("filename")

	file_path = directory + "/" + filename
	with open(file_path, 'r') as f:
		data = f.read()
		print(data)

		response = HttpResponse(data, content_type=mimetypes.guess_type(file_path)[0])
		response['Content-Disposition'] = "attachment; filename={0}".format(filename)
		response['Content-Length'] = os.path.getsize(file_path)
		return response

