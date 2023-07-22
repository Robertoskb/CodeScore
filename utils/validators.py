import zipfile

from django.core.exceptions import ValidationError
from pypdf import PdfReader
from pypdf.errors import PdfReadError


def zip_validator(value):
    try:
        with zipfile.ZipFile(value, 'r') as zip_file:
            files_in = files_out = 0

            for file in zip_file.namelist():
                if file.endswith('in'):
                    files_in += 1
                if file.endswith('out'):
                    files_out += 1

            if 0 in (files_in, files_out) or files_in != files_out:
                raise ValidationError('Gabarito inválido')

    except zipfile.BadZipFile:
        raise ValidationError('Arquivo zip inválido')

    return value


def pdf_validator(value):
    try:
        pdf_reader = PdfReader(value)
        if len(pdf_reader.pages) == 0:
            raise ValidationError('PDF inválido')

    except PdfReadError:
        raise ValidationError('PDF inválido')
