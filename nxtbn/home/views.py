from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse

# Create a view to serve robots.txt
def robots_txt(request):
    # Create the content for robots.txt
    content = (
        "User-agent: *\n"
        "Disallow: /docs/\n" 
        "Disallow: /admin/\n"
        "Disallow: /api/\n"
        "Allow: /\n"  # Allow everything else
    )
    
    return HttpResponse(content, content_type="text/plain")


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse('api_playground'))
    else:
        return redirect(reverse('account_login'))
