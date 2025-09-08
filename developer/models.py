from django.db import models


class Technology(models.Model):
    PYTHON = 'Python'
    JAVASCRIPT = 'JavaScript'
    DJANGO = 'Django'
    VUEJS = 'VueJS'
    ANGULARJS = 'AngularJS'
    POSTGRESQL = 'Postgresql'
    CPP = 'C - CPP'
    RUST = 'Rust'
    REDIS = 'Redis'
    LINUX = 'Linux'
    SOCKET_PROGRAMMING = 'Socket Programming'
    BASHSCRIPT = 'Bash Scripting'
    QT = 'Qt'
    API_DEVELOPMENT = 'API Development'
    GRAPHQL = 'GraphQL'
    TRANSLATE = 'translate'
    

    TECH = {
        (PYTHON, 'Python'), (JAVASCRIPT, 'JavaScript'), (DJANGO, 'Django'),
        (VUEJS, 'VueJS'), (ANGULARJS, 'AngularJS'), (POSTGRESQL, 'Postgresql'),
        (CPP, 'C - CPP'), (RUST, 'Rust'), (REDIS, 'Redis'), (LINUX, 'Linux'),
        (SOCKET_PROGRAMMING, 'Socket Programming'), (BASHSCRIPT, 'Bash Scripting'),
        (QT, 'Qt'), (API_DEVELOPMENT, 'API Development'),(GRAPHQL, 'GraphQL'),
        (TRANSLATE, 'translate')
        
    }
    
    
    title = models.CharField(choices=TECH, blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    
    def __str__(self):
        return self.title



class Developer(models.Model):

    BACHELOR = 'Bachelor'
    MASTER = 'Master'
    PHD = 'PhD'
    BACKEND_DEVELOPER = 'backend developer'
    SOFTWARE_ENGINEER = 'software engineer'
    TECH_GUY = 'tech guy'

    DEGREE = {
        (BACHELOR, 'Bachelor'),
        (MASTER, 'Master'),
        (PHD, 'PhD')
    }
    
    WORK_FIELD = {
        (BACKEND_DEVELOPER, 'Backend Developer'),
        (SOFTWARE_ENGINEER, 'software engineer'),
        (TECH_GUY, 'tech guy')
    }

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64, unique=True)
    work_field = models.CharField(choices=WORK_FIELD, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='developer_profile/')
    developer_resume = models.FileField(upload_to='developer_resume/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    skills = models.ManyToManyField(Technology, blank=True)
    github_link = models.CharField(max_length=256)
    lnkedin_link = models.CharField(max_length=256)
    instagram_link = models.CharField(max_length=256)
    twitter_link = models.CharField(max_length=256)
    
    country = models.CharField(max_length=64, blank=True, null=True)
    state = models.CharField(max_length=64, blank=True, null=True)
    city = models.CharField(max_length=64, blank=True, null=True)
    degree = models.CharField(choices=DEGREE, blank=True, null=True)
    
    available_to_work = models.BooleanField(default=True)
    
    

    def __str__(self):
        return self.username
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def full_address(self):
        return f"{self.country}, {self.state}, {self.city}"
    
    

class Resume(models.Model):
    
    WORK_EXPERIENCE = 'work'
    EDUCATION_EXPERIENCE = 'education'
    OPENSOURCE_PROJECT = 'open-source projects'

    EXPERIENCE_TYPE = {
        (WORK_EXPERIENCE, 'work'),
        (EDUCATION_EXPERIENCE, 'education'),
        (OPENSOURCE_PROJECT, 'open-source projects')
    }
    
    developer = models.ForeignKey(Developer, blank=True, null=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=128)
    description = models.CharField(max_length=512, blank=True, null=True)
    company = models.CharField(max_length=256, blank=True, null=True)
    academy = models.CharField(max_length=256, blank=True, null=True)
    project_link = models.CharField(max_length=256, blank=True, null=True)
    type = models.CharField(choices=EXPERIENCE_TYPE)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    
    company_phone = models.CharField(max_length=15, blank=True, null=True)
    company_email = models.EmailField(max_length=64, blank=True, null=True)
    company_country = models.CharField(max_length=64, blank=True, null=True)
    company_state = models.CharField(max_length=64, blank=True, null=True)
    company_city = models.CharField(max_length=64, blank=True, null=True)
    
    academy_phone = models.CharField(max_length=15, blank=True, null=True)
    academy_email = models.EmailField(max_length=64, blank=True, null=True)
    academy_country = models.CharField(max_length=64, blank=True, null=True)
    academy_state = models.CharField(max_length=64, blank=True, null=True)
    academy_city = models.CharField(max_length=64, blank=True, null=True)
    

    def __str__(self):
        return f"{self.developer}, {self.position}"
    
    def comapny_address(self):
        return f"{self.company_country}, {self.company_state}, {self.company_city}"
    
    def academy_address(self):
        return f"{self.academy_country}, {self.academy_state}, {self.academy_city}"
    

class Projects(models.Model):
    CLI_PROJECT = 'cli projects'
    SYSTEM_BACKEND = 'system projects'
    WEB_BACKEND = 'web back-end'
    WEB_DESIGN = 'web front-end'

    PROJECT_TYPE = {
        (CLI_PROJECT, 'cli projects'),
        (SYSTEM_BACKEND, 'system projects'),
        (WEB_BACKEND, 'web back-end'),
        (WEB_DESIGN, 'web front-end'),
    }
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    type = models.CharField(choices=PROJECT_TYPE)
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=512)
    link = models.CharField(blank=True, null=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} developed by {self.developer}"
    
    
    def first_image(self):
        return self.images.first()
    



class ProjectImage(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects_images/')
    
    def __str__(self):
        return f"image for {self.project.title}"
    