from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from nxtbn.post.models import Post
from nxtbn.product.models import Product

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



class StaticViewSitemap(Sitemap): # added for the demonstration only
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
            # 'home',
            # 'about',
            # 'contact'
        ]  # Names of views or URL names / doesn't exist yet, just for placeholder

    def location(self, item):
        return reverse(item)



class ProductSitemap(Sitemap):
    changefreq = "weekly" 
    priority = 0.7

    def items(self):
        return Product.objects.all() 

    def lastmod(self, obj):
        return obj.last_modified


class PostSitemap(Sitemap):
    changefreq = "weekly" 
    priority = 0.7

    def items(self):
        return Post.objects.all() 

    def lastmod(self, obj):
        return obj.last_modified

site_maps = {
    'static': StaticViewSitemap(),
    'product': ProductSitemap(),
    'post': PostSitemap(),
}