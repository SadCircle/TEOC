from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, DetailView
from BookReaders.read_book import *
from .models import *
from django.contrib.postgres.search import SearchVector
# Create your views here.


def index(request):
    context = {'title': 'Каталог'}
    return render(request, 'catalog/index.html', context)

class Documents(ListView):
    paginate_by = 6
    model = Document
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        return context


    def get_queryset(self):
        query = self.request.GET.get("q")
        if not query:
            return Document.objects.all()
        return Document.objects.filter(search_vector=query)

class Document_card(DetailView):
    model = Document
    template_name = 'catalog/document.html'



def upload_files(request):
    if request.method == 'POST':
        print(request.FILES)
        temp_dict = dict()
        #продумать если в базе уже есть такой файл, чтобы не сохранять его и выводить красивую ошибку
        for file in request.FILES:
            file_ = request.FILES.get(file)
            path_ = file_.temporary_file_path()
            ext_ = '.' + file_.name.split('.')[-1]
            hash_key, book_text_, image_, title_, _, author_ = take_additional_features(path_, ext_)
            temp_dict[hash_key] = {
                    'tg_hash_key': hash_key,
                    'local_hash_key': hash_key,
                    'name': file_.name,
                    'ext': ext_,
                    'size': file_.size,
                    'path': file_,
                    'description': file_.name,
                    'book_text': book_text_,
                    'image': image_,
                    'title':title_,
                    'author':author_
                }
        hash_keys_ = [local_hash_key[0] for local_hash_key in Document.objects.filter(local_hash_key__in=temp_dict.keys()).values_list('local_hash_key')]
        #для этих hash_keys сделать Raise
        keys_to_insert = list(set(temp_dict.keys()) - set(hash_keys_))
        objects_ = []
        for key in keys_to_insert:
            objects_.append(
                Document(
                    tg_hash_key=temp_dict[key]['tg_hash_key'],
                    local_hash_key=temp_dict[key]['local_hash_key'],
                    name=temp_dict[key]['name'],
                    ext=temp_dict[key]['ext'],
                    size=temp_dict[key]['size'],
                    path=temp_dict[key]['path'],
                    description=temp_dict[key]['description'],
                    book_text=temp_dict[key]['book_text'],
                    image=temp_dict[key]['image'],
                    title=temp_dict[key]['title'],
                    author=temp_dict[key]['author']
                )
            )
        Document.objects.bulk_create(objects_)
        Document.objects.update(search_vector=SearchVector("book_text"))
    return render(request, 'catalog/upload_files.html')