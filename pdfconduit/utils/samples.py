# Generate sample PDF documents
import os
from pdfconduit.utils import available_images
from pdfconduit import Label, Watermark, Merge, slicer, Info
from tests import pdf


class Samples:
    def __init__(self, src, dst):
        if not os.path.exists(dst):
            os.mkdir(dst)
        self.src = src
        self.dst = dst
        self.wm = Watermark(self.src, use_receipt=False, open_file=False, remove_temps=True)

    def _title(self, title='PDF Samples'):
        return Label(pdf, title, title_page=True, tempdir=self.wm.tempdir).watermark

    def cleanup(self):
        self.wm.cleanup()

    def watermarks(self, images=available_images()):
        watermarks = [self._title('Watermark Images')]
        for i in images:
            wm = self.wm.draw(text1=i, image=i, copyright=False)
            watermarks.append(wm)
        m = Merge(watermarks, 'Watermarks samples', self.dst)
        return m.file

    def opacity(self):
        samples = [self._title('Opacity Comparisons')]
        _range = range(4, 25)[::3]
        if Info(self.src).pages > 1:
            self.src = slicer(self.src, 1, 1, self.wm.tempdir)
        for i in _range:
            o = i * .01
            wtrmrk = self.wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', opacity=o)
            watermarked = self.wm.add(document=self.src, watermark=wtrmrk)

            labeled_pdf = Label(watermarked, str(str(i).zfill(2) + '%'), tempdir=self.wm.tempdir).write(cleanup=False)
            samples.append(labeled_pdf)
        m = Merge(samples, 'Opacity comparison samples', self.dst)
        return m.file

    def placement(self):
        if Info(self.src).pages > 2:
            self.src = slicer(self.src, 1, 1, self.wm.tempdir)
        wtrmrk = self.wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA')
        over = self.wm.add(document=self.src, watermark=wtrmrk, underneath=False)
        over_with_label = Label(over, 'Overlayed watermark', tempdir=self.wm.tempdir).write(cleanup=False)

        under = self.wm.add(document=self.src, watermark=wtrmrk, underneath=True)
        under_with_label = Label(under, 'Underneath watermarked', tempdir=self.wm.tempdir).write(cleanup=False)

        to_merge = [self._title('Watermark Placement'), over_with_label, under_with_label]
        m = Merge(to_merge, 'Watermark Placement samples', self.dst)
        return m.file

    def layering(self):
        if Info(self.src).pages > 2:
            self.src = slicer(self.src, 1, 1, self.wm.tempdir)
        flat = self.wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', flatten=True)
        layered = self.wm.draw(text1='200 Stonewall Blvd', text2='Wrentham, MA', flatten=False)

        wtrmrked_flat = Label(self.wm.add(document=self.src, watermark=flat), 'Flat watermark',
                              tempdir=self.wm.tempdir).write(cleanup=False)
        wtrmrked_layer = Label(self.wm.add(document=self.src, watermark=layered), 'Layered watermark',
                               tempdir=self.wm.tempdir).write(cleanup=False)

        watermark_flat = Label(flat, 'Flat watermark', tempdir=self.wm.tempdir).write(cleanup=False)
        watermark_layer = Label(layered, 'Layered watermark', tempdir=self.wm.tempdir).write(cleanup=False)

        to_merge = [self._title('Watermark Layering'), wtrmrked_flat, watermark_flat, wtrmrked_layer, watermark_layer]
        m = Merge(to_merge, 'Layering samples', self.dst)
        return m.file


def main():
    src = pdf
    dst = os.path.join(os.path.dirname(src), 'samples')

    s = Samples(src, dst)
    s.opacity()
    s.watermarks()
    s.placement()
    s.layering()

    s.cleanup()


if __name__ == '__main__':
    main()
