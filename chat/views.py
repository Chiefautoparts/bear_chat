from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	rooms = Room.objects.order_by("title")
	return render(request, "index.html", {"rooms": rooms, 
		})