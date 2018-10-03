from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
# from reportlab.pdfgen import canvas
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *

# from io import BytesIO
from reportlab.pdfgen import canvas

from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import *
# from threading import Thread, activeCount
# from django.core.mail import EmailMessage


def add(request):
    data = Pdf.objects.all()
    if request.method == 'POST':
        form = PdfForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PdfForm()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'pdf/add.html', context)


def pdf_details(request, slug):
    instance = get_object_or_404(Pdf, slug=slug)
    context = {
        'instance': instance
    }
    return render(request, 'pdf/pdf_details.html', context)


class PdfView(View):

    def get(self, request, slug):
        instance = get_object_or_404(Pdf, slug=slug)
        today = timezone.now()
        params = {
            'instance': instance,
            'today': today,
            'request': request
        }

        file = Render.render_to_file('pdf/pdf_template.html', params)
        # name = str(file[0])
        # name1 = name[0:len(name)-4]
        return Render.render('pdf/pdf_template.html', params)


