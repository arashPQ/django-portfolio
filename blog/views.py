from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator

from blog.models import Article, Author, Tags, SubTitle
from blog.forms import ArticleForm
from developer.models import Developer

developer = Developer.objects.get(username='arashPQ')


def superuser_required(func):
    decorator = user_passes_test(lambda u:u.is_superuser)
    return decorator(func)


def blog(request):
    return redirect('blog:article_list')


@superuser_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()

        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        published = request.POST.get('published') == 'on'
        author_id = request.POST.get('author')
        author = Author.objects.get(id=author_id)
        slug = slugify(title) + '-' + str(author_id)

        tag_ids = request.POST.getlist('tags')
        
        subtitles = request.POST.getlist('subtitle[]')
        bodies = request.POST.getlist('body[]')
        sections = [
            {'subtitle': subtitle, 'body': body, 'type': 'text'}
            for subtitle, body in zip(subtitles, bodies)
        ]
        article = Article.objects.create(
            title=title,
            description=description,
            author=author,
            image=image,
            published=published,
            article={'sections': sections}
        )
        article.slug = slug
        article.tag.set(tag_ids)
        article.save()
        return redirect('blog:article_list')  
            
    else:
        form = ArticleForm()
    tags = Tags.objects.all()
    authors = Author.objects.all()
    data = {
        'form': form,
        'tags': tags,
        'authors': authors,
        'developer': developer,
    }
    return render(request, 'blog/create_article.html', data)


def article_list(request):
    articles = Article.objects.filter(published=True).order_by('-created_at')
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    data = {
        'articles': articles,
        'developer': developer,
        'page_objects': page_objects,
    }
    return render(request, 'blog/index.html', data)


def article_detail(request, pk=None):
    article = Article.objects.get(pk=pk)
    subtitles = SubTitle.objects.filter(article=article)
    tags = article.tag.all()
    data = {
        'developer': developer,
        'article': article,
        'subtitles': subtitles,
        'tags': tags
    }
    return render(request, 'blog/article_detail.html', data)


def SearchByTag(request, tt):
    tt = tt.replace('-', ' ')
    articles = Article.objects.filter(Q(tag__title__icontains=tt, published=True)).order_by('-created_at')
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    if not articles:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('blog:article_list')
    else:
        return render(request, 'blog/bytag.html', {
            'developer': developer,
            'articles': articles,
            'page_objects': page_objects,
            'tag': tt,
        })