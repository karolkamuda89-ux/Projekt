from django.shortcuts import render

def index(request):
    return render(request, "datasets/index.html")
def upload_csv(request):
    return render(request, 'datasets/upload.html')
def file_list(request):
    return render(request, 'datasets/list.html')
def file_detail(request):
    return render(request, 'datasets/detail.html')
def detail(request, plik_id):
    context = {'plik': {'id': plik_id, 'nazwa': f'Plik_nr_{plik_id}.csv'}}
    return render(request, 'datasets/detail.html', context)