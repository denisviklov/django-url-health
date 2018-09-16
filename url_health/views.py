from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from jsonview.decorators import json_view

from .models import LinkStore, Scanning
from .forms import URLForm
from .tasks import scan_links


@login_required
def index(request):
    form = URLForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'url_health/linkcheck.html',
                {'links': LinkStore.objects.all(), 'form': form}
            )


@login_required
def scan(request):
    LinkStore.objects.all().update(status=0)
    print(request.META['HTTP_HOST'])
    scan_links.delay(request.META['HTTP_HOST'])
    return redirect('scan_results')


@login_required
def scan_results(request):
    return render(request, 'url_health/linkcheck_done.html',
                {'results': LinkStore.objects.exclude(status=0)}
            )


@login_required
@json_view
def poll_results(request):
    links = LinkStore.objects.exclude(status=0)
    stop = True
    html = render_to_string(
        'url_health/link_check_table.html',
        {'results': links}
        )

    if Scanning.objects.first().status:
        stop = False

    return {'html': html, 'stop': stop}


@login_required
def delete_url(request, id):
    LinkStore.objects.get(id=id).delete()
    return redirect('index')


@json_view
def fetch_links(request):
    return {
        'status': True,
        'links': [link_obj.link for link_obj in LinkStore.objects.all()]
        }


@csrf_exempt
@json_view
def post_link_info(request):
    print(request.POST.get('link'))
    instance = get_object_or_404(LinkStore, link=request.POST.get('link'))
    form = URLForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
    return {'success': True}