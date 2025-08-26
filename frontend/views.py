from .forms import LoginForm
from django. contrib import messages 
import requests
from django.shortcuts import render, redirect
import requests
from .forms import ProjectForm
from django.shortcuts import HttpResponse

API_BASE_URL = 'http://127.0.0.1:8000/api/projects/'



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Login credentials:", username, password)


        # Send credentials to JWT endpoint
        response = requests.post('http://127.0.0.1:8000/api/token/', data={
            'username': username,
            'password': password,
        })
        print('Printing First 1')
        print("Response status:", response.status_code)
        print("Response body:", response.text)
        if response.status_code == 200:
            tokens = response.json()
            print('Printing First 2')
            request.session['access_token'] = tokens['access']
            request.session['refresh_token'] = tokens['refresh']
            print("Response status:", response.status_code)
            print("Response body:", response.text)
            return redirect('project_list')  # Replace with your actual page
        else:
            # print("Response status:", response.status_code)
            # print("Response body:", response.text)
            messages.error(request, "Invalid username or password")

    return render(request, 'frontend/login.html')
def logout_view(request):
    request.session.flush()  # clear all session data
    return redirect('login')


def project_list(request):
    access_token = request.session.get('access_token')

    if not access_token:
        return redirect('login')

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Get current user info
    user_response = requests.get('http://127.0.0.1:8000/auth/api/me/', headers=headers)
    if user_response.status_code == 200:
        user_info = user_response.json()
        print("Logged-in user:", user_info['username'])
    else:
        print("Failed to get user info")


    page = request.GET.get('page', 1)
    response = requests.get(f"{API_BASE_URL}?page={page}", headers=headers)

    
    # if request.user.is_authenticated:
    #     print('Logged-in user:', request.user.username)
    # else:
    #     print('User is not authenticated')
    if response.status_code == 200:
        data = response.json()
        projects = data.get('results', data)  # handle both paginated and full response
        return render(request, 'frontend/project_list.html', {
            'projects': projects,
            'next_page': data.get('next'),
            'previous_page': data.get('previous'),
            'current_page': page
        })
    elif response.status_code == 401:
        # Token expired or invalid
        request.session.flush()
        return redirect('login')

    else:
        return render(request, 'frontend/project_list.html', {'projects': [], 'error': 'Failed to load projects'})



def project_create(request):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            headers = {'Authorization': f'Bearer {access_token}'}
            data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'is_private': form.cleaned_data['is_private'],
            }
            response = requests.post(API_BASE_URL, headers=headers, data=data)
            if response.status_code == 201:
                return redirect('project_list')
            else:
                form.add_error(None, 'Failed to create project')
    else:
        form = ProjectForm()

    return render(request, 'frontend/project_create.html', {'form': form})

def project_update(request, project_id):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {access_token}'}
    project_url = f"{API_BASE_URL}{project_id}/"

    # Fetch existing project data to pre-fill the form
    response = requests.get(project_url, headers=headers)

    if response.status_code != 200:
        return redirect('project_list')

    project_data = response.json()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            updated_data = {
                'title': form.cleaned_data['title'],
                'description': form.cleaned_data['description'],
                'is_private': form.cleaned_data['is_private'],
            }
            update_response = requests.put(project_url, headers=headers, data=updated_data)
            if update_response.status_code in [200, 202]:
                return redirect('project_list')
            else:
                form.add_error(None, 'Failed to update project')
    else:
        form = ProjectForm(initial={
            'title': project_data['title'],
            'description': project_data['description'],
            'is_private': project_data['is_private'],
        })

    return render(request, 'frontend/project_update.html', {'form': form, 'project_id': project_id})


def project_delete(request, project_id):
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    headers = {'Authorization': f'Bearer {access_token}'}
    project_url = f"{API_BASE_URL}{project_id}/"
    print('printing project url', project_url)

    # Only allow POST for deletion (avoid GET delete for safety)
    if request.method == 'POST':
        response = requests.delete(project_url, headers=headers)
        print('printing the status code', response.status_code)
        if response.status_code == 204:
            return redirect('project_list')
        else:
            return HttpResponse("Failed to delete project", status=400)

    return render(request, 'frontend/project_confirm_delete.html', {'project_id': project_id})

