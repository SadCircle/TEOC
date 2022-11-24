from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
#from .tasks import get_documents
# Create your models here.


class Document(models.Model):
    tg_hash_key = models.CharField(max_length=255, unique=True)
    local_hash_key = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    path = models.FileField(upload_to='documents/', max_length=255, null=True,blank=True,default=None)
    description = models.TextField( null=True,blank=True, default=None)

    class Extention(models.TextChoices):
        pdf = '.pdf'
        epub = '.epub'
        fb2 = '.fb2'
        djvu = '.djvu'
        txt = '.txt'
        unknow = 'unknow'

    ext = models.CharField(
        max_length=10,
        choices=Extention.choices,
        default=Extention.unknow,
    )
    image = models.ImageField(upload_to='images/',
                              max_length=255,
                              default='images/no_photo.jpg')
    language = models.ForeignKey('Language',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 default=None)                             
    author = models.CharField(max_length=255, blank=True, null=True, default=None)
    title = models.CharField(max_length=255, blank=True, null=True, default=None)
    tags = models.ManyToManyField('Tag', blank=True, default=None)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    book_text = models.TextField(default='')
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = (GinIndex(fields=["search_vector"]),)

    def __str__(self):
        return self.name

    def create_document(self, data):
        item = Document.objects.get_or_create(
            tg_hash_key=data['tg_hash_key'],
            name=data['name'],
            size=data['size'],
            path=data['path'],
            description=data['description'],
            ext=data['ext'],
        )
        if item:
            print(f'Document {item.tg_hash_key} has already existed')


class Language(models.Model):
    code = models.CharField(max_length=4)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return (self.full_name)


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
