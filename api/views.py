from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os, mimetypes
import fuzzyset

THRESHOLD = 0.3
DIFFERENCE_THRESHOLD = .05

# Index the lines in all our subtitles once upon deploy
directory = os.path.dirname(os.path.realpath(__file__)) + "/../data"
index = 0
sets = {}
for filename in os.listdir(directory):
	if filename[0] == ".":
		continue
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
	second_accurate = None
	second_file = None
	for file in sets:
		if accurate == None:
			accurate = sets[file].get(query)[0]
			accurate_file = file
		else:
			current = sets[file].get(query)[0]
			current_file = file
			if current[0] > accurate[0]:
				second_accurate = accurate
				second_file = accurate_file
				accurate = current
				accurate_file = current_file
	
	if accurate[0] < THRESHOLD or (accurate[0] - second_accurate[0]) < DIFFERENCE_THRESHOLD:
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
	targetLine = request.GET.get("targetLine")

	data = []
	file_path = directory + "/" + filename
	with open(file_path, 'r') as f:
		current = {"lines": []}
		count = -1
		index_count = 0
		for line in f:
			count += 1
			line = line.strip()
			if count == 0:
				continue
			elif count == 1:
				time_raw = line.split(" --> ")
				current["start"] = convert(time_raw[0])
				current["end"] = convert(time_raw[1])
			elif line == "":
				count = -1
				print(current)
				print()
				print()
				data.append(current)
				current = {"lines": []}
				continue
			else:
				current["lines"].append(line)
				if targetLine == line:
					index = index_count
				else:
					index_count += 1

		return JsonResponse({
			"status": "success",
			"data": {"array": data, "index":index}
		})

def convert(string):
	# 00:00:39,444
	hour = int(string[0:2])
	min = int(string[3:5])
	sec = int(string[6:8])
	mil = int(string[9:])
	return mil + sec * 1000 + min * 60 * 1000 + hour * 3600 * 1000

