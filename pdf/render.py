from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
from random import randint
from django.core.mail import EmailMessage


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            # print(response.getvalue())
            email = EmailMessage('subject', 'message',
                                 ['harshit8858@gmail.com'], ['harshit8858@gmail.com'])
            email.attach('Report.pdf', response.getvalue(), "application/pdf")
            email.send()
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}-{1}.pdf".format(params['request'].user.first_name, randint(1, 1000000))
        file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), "store", file_name)
        # file_path = os.path.join(os.path.abspath(os.path.dirname("__file__")), , file_name)
        with open(file_path, 'wb') as pdf:
            x = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]