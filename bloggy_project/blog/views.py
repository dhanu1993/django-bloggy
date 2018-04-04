from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

from blog.models import Post 
from blog.forms import PostForm

# helper functions
def encode_url(url):
	return url.replace(' ', '_')

def index(request):
	latest_posts = Post.objects.all().order_by('-created_at')
	popular_posts = Post.objects.order_by('-views')[:5]
	t = loader.get_template('blog/index.html')
	context_dict = {
		'latest_posts':latest_posts,
		'popular_posts':popular_posts,
	}

	for post in latest_posts:
		post.url = encode_url(post.title)

	for post in popular_posts:
		post.url = encode_url(post.title)

	c = Context(context_dict)
	return HttpResponse(t.render(c))

def post(request, slug):
	single_post = get_object_or_404(Post, slug=slug)
	single_post.views += 1
	single_post.save()
	t = loader.get_template('blog/post.html')
	c = Context({ 'single_post':single_post, })
	return HttpResponse(t.render(c))	

def add_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			return redirect(index)
		else:
			print(form.errors)
	else:
		form = PostForm()
	return render(request, 'blog/add_post.html', {'form':form})
