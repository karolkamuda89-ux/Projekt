from django.shortcuts import render

def index(request):
    return render(request, "datasets/index.html")
def upload_csv(request):
    return render(request, 'datasets/upload.html')