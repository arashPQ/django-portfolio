from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from developer.models import Developer, Resume, Technology
from blog.models import Article, Tags

tech = Tags.objects.all().order_by('id')[:5]


def portfolio(request):
    developer = Developer.objects.get(username='arashPQ')
    resume = Resume.objects.filter(developer=developer)

    data = {
        'developer': developer,
        'experiences': resume.filter(type='work'),
        'educations': resume.filter(type='education'),
        'projects': resume.filter(type='open-source projects'),
        'skills': developer.skills.all(),
        'tech': tech
    }
    
    return render(request, 'developer/index.html', data)


def SearchByTag(request, tt):
    tt = tt.replace('-', ' ')
    articles = Article.objects.filter(Q(tag__title__icontains=tt, published=True)).order_by('-created_at')
    if not articles:
        messages.warning(request, ("Sorry!! somethig wrong ..."))
        return redirect('blog:article_list')
    else:
        return render(request, 'blog/bytag.html', {
            'articles': articles,
            'tag': tt,
        })