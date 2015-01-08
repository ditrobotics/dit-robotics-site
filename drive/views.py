from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import itertools

from drs import settings

from .forms import UploadFileForm
from .models import DriveFile, DriveDirectory, DriveRootDirectory
# Create your views here.

def errors_to_string(errors):
    return '; '.join(
        map(
            str,
            itertools.chain(
                *itertools.chain(
                    *errors.as_data().values()
                )
            )
        )
    )

@login_required
def drive(request):
    if request.user.profile.access_level < 2:
        return render_to_response('drive_member_required.html', RequestContext(request))
    return redirect(DriveRootDirectory(user=request.user).reverse)

def locate_dpath(user, path):
    first, *path = path.strip('/').split('/')
    result = get_object_or_404(DriveDirectory, user=user, parent=None, name=first)
    for sub in path:
        result = result.subdirectories.get(name=sub)
    return result

def listing(request, args):
    username, _, path = args.partition('/')
    user = get_object_or_404(User, username=username)
    if path:
        directory = locate_dpath(user, path)
    else:
        directory = DriveRootDirectory(user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            drive_file = form.save(commit=False)
            drive_file.filename = request.FILES['file']
            drive_file.user = request.user
            if isinstance(directory, DriveDirectory):
                drive_file.parent = directory
            drive_file.save()
            return redirect('drive')
        else:
            if request.META.get('HTTP_DROPZONE_IDENTIFIER', None) == 'driveDropzone':
                return HttpResponse(
                    errors_to_string(form.errors),
                    status=422
                )
    else:
        form = UploadFileForm()
    context = RequestContext(request)
    context['directory'] = directory
    context['form'] = form
    files = DriveFile.objects.filter(user=directory.user)
    context['files'] = files
    context['usage'] = sum(f.file.size for f in files)
    return render_to_response('drive.html', context)

def get(request, id, filename):
    drive_file = get_object_or_404(DriveFile, id=id, filename=filename)
    if drive_file.user != request.user:
        return render_to_response('drive_denied.html', RequestContext(request))
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment'
    if settings.DEBUG:
        response.content = drive_file.file.read()
    else:
        response['X-Accel-Redirect'] = drive_file.file.url
    return response

def delete(request, id):
    drive_file = get_object_or_404(DriveFile, id=id)
    if drive_file.user != request.user:
        return render_to_response('drive_denied.html', RequestContext(request))
    drive_file.delete()
    return redirect('drive')
