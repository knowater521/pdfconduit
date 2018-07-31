# Apply a watermark to a PDF file
import os
import shutil
import warnings
from datetime import datetime
from pdfwatermarker.watermark.draw import WatermarkDraw
from pdfwatermarker.watermark.add import WatermarkAdd
from pdfwatermarker import add_suffix, open_window, protect
from looptools import Timer


def remove_temp(pdf):
    temp = os.path.join(os.path.dirname(pdf), 'temp')
    shutil.rmtree(temp)


class Watermark:
    def __init__(self, pdf, project, address, town, state, opacity=0.1, encrypt=None, encrypt_128=True,
                 remove_temps=True):
        text = {
            'address': {
                'font': 40,
                'y': -140,
                'txt': {'address': address,
                        'town': town,
                        'state': state}
            },
            'copyright': {
                'font': 16,
                'y': 10,
                'txt': '© copyright ' + str(datetime.now().year),
            }
        }
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            watermark = str(WatermarkDraw(project, text, pdf, opacity=opacity))
        self.pdf = WatermarkAdd(pdf, watermark)
        open_window(self.pdf)

        if encrypt:
            secure_pdf = protect(str(self.pdf), encrypt.user_pw, owner_pw=encrypt.owner_pw, output=encrypt.output,
                                 encrypt_128=encrypt_128)
            self.pdf = secure_pdf

        if remove_temps:
            remove_temp(pdf)

        # Open watermarked PDF in finder or explorer window
        open_window(self.pdf)

    def __str__(self):
        return str(self.pdf)


class WatermarkGUI:
    def __init__(self):
        # Import GUI and timeout libraries
        from pdfwatermarker.watermark.lib import GUI
        import datetime
        time = Timer()
        now = datetime.datetime.now()
        self.receipt = []
        self.receipt_add('PDF Watermarker', now.strftime("%Y-%m-%d %H:%M"))

        pdf, address, town, state, encrypt, opacity, user_pw, owner_pw = GUI().settings
        project = os.path.basename(pdf)[:8]

        # Print GUI selections to console
        self.receipt_add('Directory', os.path.dirname(pdf))
        self.receipt_add('PDF', os.path.basename(pdf))
        self.receipt_add('Project', project)
        self.receipt_add('Address', address)
        self.receipt_add('Town', town)
        self.receipt_add('State', state)
        self.receipt_add('WM Opacity', str(int(opacity * 100)) + '%')
        self.receipt_add('User pw', user_pw)
        self.receipt_add('Owner pw', owner_pw)

        # Execute Watermark class
        wm = Watermark(pdf, project, address, town, state, opacity)
        self.receipt_add('Watermarked PDF', os.path.basename(str(wm)))

        if encrypt:
            output = add_suffix(pdf, 'secured')
            self.pdf = protect(str(wm), user_pw, owner_pw, output=output)
            print("{0:20}--> {1}".format('Secured PDF', os.path.basename(self.pdf)))

        runtime = time.end
        self.receipt_add('~run time~', runtime)

        try:
            self.receipt_dump()
            print('\nSuccess!')
            input('~~Press Any Key To Exit~~')
        except RuntimeError:
            quit()

    def receipt_add(self, key, value):
        message = str("{0:20}--> {1}".format(key, value))
        print(message)
        self.receipt.append(message)

    def receipt_dump(self):
        file_name = os.path.join(os.path.dirname(self.pdf), 'watermark receipt.txt')
        exists = os.path.isfile(file_name)
        with open(file_name, 'a') as f:
            if exists:
                f.write('*******************************************************************\n')

            for item in self.receipt:
                f.write(item + '\n')
