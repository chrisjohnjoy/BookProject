from django.shortcuts import render,redirect
from django.urls import reverse_lazy
# Create your views here.
from .models import *
from django.views.generic import CreateView,ListView
from .forms import AuthorForm,BookForm
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout

def create(req):

    books=Book.objects.all()
    if req.method=='POST':
        form=BookForm(req.POST,req.FILES)

        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form=BookForm()

    return render(req,'books.html',{'form':form,'books':books})

# def create(req):
#     books=Book.objects.all()

#     if req.method=='POST':
#         title=req.POST.get('title')
#         price=req.POST.get('price')

#         book=Book(title=title,price=price)
        
#         book.save()

#     return render(req,'books.html',{'books':books})

def createAuthor(req):
    if req.method=='POST':
        form=AuthorForm(req.POST)

        if form.is_valid():
            form.save()
        return redirect('/')
    else:
        form=AuthorForm()

    return render(req,'author.html',{'form':form})

def listBook(req):
    books=Book.objects.all().order_by('author')
    paginator=Paginator(books,4)
    pagenumber=req.GET.get('page')


    try:
        page=paginator.get_page(pagenumber)
    except EmptyPage:
        page=paginator.page(pagenumber.num_pages)

    return render(req,'listbook.html',{'books':books,'page':page})

def detailsview(req,book_id):
    book=Book.objects.get(id=book_id)

    return render(req,'detailsview.html',{'book':book})


def updatebook(req,book_id):

    book=Book.objects.get(id=book_id)
    if req.method=='POST':
        form=BookForm(req.POST,req.FILES,instance=book)
        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form=BookForm(instance=book)

    return render(req,'updateview.html',{'form':form,'book':book})

# def updatebook(req,book_id):

#     book=Book.objects.get(id=book_id)

#     if req.method=='POST':
#         title=req.POST.get('title')
#         price=req.POST.get('price')

#         book.title=title
#         book.price=price
#         book.save()
#         return redirect ('/')

#     return render(req,'updateview.html',{'book':book})


def deleteview(req,book_id):
    book=Book.objects.get(id=book_id)
    if req.method=='POST':
        book.delete()

        return redirect('/')
    return render(req,'deleteview.html',{'book':book})

# class BookCreationView(CreateView):
    
#     model=Book
#     template_name='home.html'

#     fields=['title','price'] '__all__'

#     success_url=reverse_lazy('booklist')

# class BookListView(ListView):

#     models=Book
#     template_name='listview.hmtl'

#     context_object_name='book'

def index(req):
    return render(req,'base.html')

# role based authentication

def search_book(req):
    query=None
    books=None

    if 'q' in req.GET:

        query=req.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    else:
        books=[]
    context={'books':books,'query':query}

    return render(req,'search.html',context)





