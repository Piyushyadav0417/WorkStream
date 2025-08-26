from django.http import JsonResponse
from django.urls import resolve
from projects.models import Project
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class NotificationAccessControlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        print("Middleware initialized")

    def __call__(self, request):
        path = request.path
        # print("Middleware called — path:", path)
        
        if path.startswith('/api/notifications/'):
            print("Middleware matched notifications path")

            # Extract and set request.user using JWT manually
            try:
                user_auth_tuple = JWTAuthentication().authenticate(request)
                if user_auth_tuple is not None:
                    request.user, _ = user_auth_tuple
                    print("Authenticated user:", request.user)
                else:
                    return JsonResponse({'detail': 'Authentication credentials were not provided.'}, status=401)
            except AuthenticationFailed:
                return JsonResponse({'detail': 'Invalid or expired token.'}, status=401)

            # Resolve project ID
            resolver_match = resolve(path)
            project_id = resolver_match.kwargs.get('project_id')
            print("Resolved project_id:", project_id)

            if project_id:
                try:
                    project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    return JsonResponse({'detail': 'Project not found.'}, status=404)

                # Check if the request user is the project owner
                if project.owner != request.user:
                    print("Access denied: Not the project owner")
                    return JsonResponse({'detail': 'Access denied. Only the project owner can access this.'}, status=403)

        return self.get_response(request)
