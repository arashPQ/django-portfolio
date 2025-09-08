from django.shortcuts import render, redirect
from developer.models import Developer, Resume, Projects, ProjectImage


def projects(request):
    redirect('developer:index')


def portfolio(request):
    developer = Developer.objects.get(username='arashPQ')
    resume = Resume.objects.filter(developer=developer)
    projects = Projects.objects.filter(developer=developer)
    data = {
        'developer': developer,
        'experiences': resume.filter(type='work'),
        'educations': resume.filter(type='education'),
        'projects': resume.filter(type='open-source projects'),
        'skills': developer.skills.all(),
        'projects': projects,
    }
    
    return render(request, 'developer/index.html', data)


def project_detail(request, pk=None):
    developer = Developer.objects.get(username='arashPQ')
    project = Projects.objects.get(pk=pk)

    imgs = ProjectImage.objects.filter(project=project)
    
    data = {
        'developer': developer,
        'project': project,
        'imgs': imgs
    }
    
    return render(request, 'developer/project_detail.html', data)