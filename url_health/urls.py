from django.urls import path, re_path

from url_health import views


urlpatterns = [
           path('', views.index, name='index'),
           path('scan/', views.scan, name='scan'),
           re_path(r'^delete/(?P<id>\d+)/$', views.delete_url, name='delete_url'),
           path('fetch-links/', views.fetch_links, name='fetch_links'),
           path('post-link-info/', views.post_link_info, name='post_link_info'),
           path('scan-results/', views.scan_results, name='scan_results'),
           path('poll-results/', views.poll_results, name='poll_results'),
        ]