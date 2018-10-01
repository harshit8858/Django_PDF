from django.shortcuts import render, get_object_or_404
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


def write_pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response