from django.shortcuts import render

# Create your views here.
def com(request):
    return render(request, 'comments/comment_temp.html')

