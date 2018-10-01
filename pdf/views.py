from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import *


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


# def write_pdf_view(request, slug):
#     instance = get_object_or_404(Pdf, slug=slug)
#     data = Pdf.objects.all()
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
#     html_string = render_to_string('pdf/pdf_template.html', {'paragraphs': data})
#
#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#
#     # Start writing the PDF here
#     p.drawString(200, 600, html_string)
#     # End writing
#
#     p.showPage()
#     p.save()
#
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#
#     return response

from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import Render

class PdfView(View):
    def get(self, request, slug):
        instance = get_object_or_404(Pdf, slug=slug)
        data = Pdf.objects.all()
        sales = Pdf.objects.all()
        today = timezone.now()
        params = {
            'instance': instance,
            'data': data,
            'today': today,
            'sales': sales,
            'request': request
        }
        return Render.render('pdf/pdf_template.html', params)


from django.core.mail import send_mail


def mail(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )

# from django.core.files.storage import FileSystemStorage
# from django.template.loader import render_to_string
#
# from weasyprint import HTML
#
# def html_to_pdf_view(request):
#     paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
#     html_string = render_to_string('pdf/pdf_template.html', {'paragraphs': paragraphs})
#
#     html = HTML(string=html_string)
#     html.write_pdf(target='/tmp/mypdf.pdf');
#
#     fs = FileSystemStorage('/tmp')
#     with fs.open('mypdf.pdf') as pdf:
#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
#         return response
#     return response