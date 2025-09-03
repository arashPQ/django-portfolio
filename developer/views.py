from django.shortcuts import render

from developer.models import Developer, Resume


def portfolio(request):
    
    
    developer = Developer.objects.get(username='arashPQ')
    resume = Resume.objects.filter(developer=developer)
    
    print (resume.filter(type='education'))
    
    data = {
        'developer': developer,
        'experiences': resume.filter(type='work'),
        'educations': resume.filter(type='education'),
        'projects': resume.filter(type='open-source projects')
    }
    
    return render(request, 'developer/index.html', data)