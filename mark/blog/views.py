from django.shortcuts import render
from django.http import HttpResponse 
from django.views.generic import (
    ListView , 
    DetailView ,
    CreateView ,
    UpdateView ,
    DeleteView
    )

from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin

# Create your views here.


# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]

from .models import Post


def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request,'blog/home.html',context)



class PostListView(ListView):
    model = Post 
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ### this line bcz we want our html should read mode as posts
    ordering = ['-date_posted']
    ### this line because we want to see our post order in descending ie newest to older

class PostDetailView(DetailView):
    model = Post 
    

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post 

    fields = ['title','content']

    def form_valid(self, form,) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form,) -> HttpResponse:
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    ## user want to update is the autor of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False
    
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post 

    success_url = '/'

    ## user want to delete is the autor of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False
      
     








def about(request):
    return render(request,'blog/about.html',{'title':"about"})