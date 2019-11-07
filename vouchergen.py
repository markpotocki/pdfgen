import pdfrw

TEMPLATE_PATH = 'template.pdf'
OUTPUT_DIR = 'output'

VOUCHER_FIELD = '/VOUCHER'


def write_pdf(outfile, voucherNumber):
    template_pdf = pdfrw.PdfReader(TEMPLATE_PATH)

    # fill in the form field
    template_pdf.Root.Pages.Kids[0].Annots[0].update(pdfrw.PdfDict(V=voucherNumber))

    # write the file
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(outfile, template_pdf)