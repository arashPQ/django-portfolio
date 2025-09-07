from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.template.defaultfilters import slugify

from blog.models import Article, Author, Tags, SubTitle
from blog.forms import ArticleForm

footer_tags = Tags.objects.all().order_by('id')[:5]

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()
        # دریافت داده‌های فرم
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # توجه: از request.FILES استفاده کنید
        published = request.POST.get('published') == 'on'  # تبدیل به boolean
        author_id = request.POST.get('author')
        author = Author.objects.get(id=author_id)
        slug = slugify(title) + '-' + str(author_id)
        # دریافت تگ‌ها (آرایه‌ای از ID تگ‌ها)
        tag_ids = request.POST.getlist('tags')
        
        # ساختار sections
        subtitles = request.POST.getlist('subtitle[]')
        bodies = request.POST.getlist('body[]')
        sections = [
            {'subtitle': subtitle, 'body': body, 'type': 'text'}
            for subtitle, body in zip(subtitles, bodies)
        ]
        # ایجاد مقاله
        article = Article.objects.create(
            title=title,
            description=description,
            author=author,
            image=image,
            published=published,
            article={'sections': sections}
        )
        article.slug = slug
        # افزودن تگ‌ها (پس از ذخیره مقاله)
        article.tag.set(tag_ids)  # set() برای ارتباط Many-to-Many
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
        'footer_tags': footer_tags
    }
    return render(request, 'blog/create_article.html', data)


def article_list(request):
    articles = Article.objects.filter(published=True).order_by('updated_at')
    data = {
        'articles': articles,
        'footer_tags': footer_tags
    }
    return render(request, 'blog/index.html', data)


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    subtitles = SubTitle.objects.filter(article=article)
    tags = article.tag.all()
    data = {
        'article': article,
        'subtitles': subtitles,
        'footer_tags': footer_tags,
        'tags': tags
    }
    return render(request, 'blog/article_detail.html', data)






def ArticleDetail(request, pk=None):
    article = Article.objects.get(pk=pk)
    subtitles = SubTitle.objects.filter(article=article)
    tags = article.tag.all()
    data = {
        'article': article,
        'subtitles': subtitles,
        'footer_tags': footer_tags,
        'tags': tags
    }
    return render(request, 'blog/article_detail.html', data)


def SearchByTag(request, tt):
    tt = tt.replace('-', ' ')
    articles = Article.objects.filter(Q(tag__title__icontains=tt, published=True)).order_by('updated_at')
    if not articles:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('core:index')
    else:
        return render(request, 'blog/tags.html', {
            'articles': articles,
            'tag': tt,
            'footer_tags': footer_tags
        })