from django.http import HttpResponse
from django.shortcuts import render

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
