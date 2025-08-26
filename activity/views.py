from django.shortcuts import render

# Create your views here.
def activity_test(request):
    return render(request, 'activity/activity_home.html')