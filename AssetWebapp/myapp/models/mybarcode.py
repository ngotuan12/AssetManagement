#    mybarcode.py
from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing,qr
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart

class MyBarcodeDrawing(Drawing):
    def __init__(self, text_value, *args, **kw):
        barcode = createBarcodeDrawing('Code128', value=text_value,  width=1000*mm,height=500*mm,barHeight=10*mm, humanReadable=True)
        Drawing.__init__(self,barcode.width,barcode.height,*args,**kw)       
        self.add(barcode, name='barcode')
        
class MyQRcodeDrawing(Drawing):
    def __init__(self, text_value, *args, **kw):
        qr_code = qr.QrCodeWidget( text_value )
        Drawing.__init__(self, width=100, height=100)
        self.add(qr_code, name='qr_code')
if __name__=='__main__':
    #use the standard 'save' method to save barcode.gif, barcode.pdf etc
    #for quick feedback while working.
    MyBarcodeDrawing("HELLO WORLD").save(formats=['gif','pdf'],outDir='.',fnRoot='barcode')