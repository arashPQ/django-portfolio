from django.shortcuts import render
from django.core.paginator import Paginator

from developer.models import Developer, Resume, Projects, ProjectImage

def get_developer():
    return Developer.objects.filter(username='arashPQ').first()

def portfolio(request):
    
    resume = Resume.objects.filter(developer=get_developer())
    OS_projects = Projects.objects.filter(developer=get_developer())
    allprojects = Projects.objects.filter(developer=get_developer()).order_by('-modified_at')[:3]
    data = {
        'developer': get_developer(),
        'experiences': resume.filter(type='work'),
        'educations': resume.filter(type='education'),
        'os_projects': OS_projects.filter(type='open source'),
        'skills': get_developer().skills.all(),
        'projects': allprojects,
    }
    
    return render(request, 'developer/index.html', data)


def projects(request):
    projects = Projects.objects.filter(developer=get_developer()).order_by('-modified_at')
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)
    data = {
        'projects': projects,
        'developer': get_developer(),
        'page_objects': page_objects,
    }
    return render(request, 'developer/projects.html', data)



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