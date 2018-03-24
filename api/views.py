from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def subs(request):
	if request.method != "GET":
		return JsonResponse({
			"status": "error",
			"data": "Use a GET request."
		})

	imdb_id = request.GET.get("imdb_id")
	

	return JsonResponse({
		"status": "success",
		"data": imdb_id
	})