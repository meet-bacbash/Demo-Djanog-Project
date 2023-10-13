from django.http import HttpResponse
import os

def myscheduledjob(name=None, iterate=10):
    for i in range(iterate):
        print(f"hello {name} {i}")
        os.mkdir(f'/tmp/{i}.txt')
    return HttpResponse("job..")
