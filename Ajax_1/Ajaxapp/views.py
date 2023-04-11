from django.shortcuts import render
from django.http import HttpResponse
from .forms import AjaxForm
from .models import Ajax_data

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def Ajax_view(request):
    print("python")
    form = AjaxForm()
    if request.method == "POST":
        print("hi")
        form = AjaxForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            data = Ajax_data.objects.all()
            print(data)
            return render(request, "Ajax.html", {"form": data})

    return render(request, "Ajax.html", {"form": form})
