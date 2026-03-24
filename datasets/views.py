from django.shortcuts import render
from .utils import get_statistics
from .models import Dataset
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, "datasets/index.html")

def upload_csv(request):
    return render(request, 'datasets/upload.html')

def file_list(request):
    return render(request, 'datasets/list.html')

def dataset_detail(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)
    stats = get_statistics(dataset.file.path)
    return render(request, 'datasets/detail.html', {'dataset': dataset, 'stats': stats})