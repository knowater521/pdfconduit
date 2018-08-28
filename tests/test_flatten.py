import unittest
import os
import shutil
import time
from pdf.conduit import Info, Flatten
from tests import directory


class TestFlatten(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Destination directory
        results = os.path.join(directory, 'results')
        if not os.path.isdir(results):
            os.mkdir(results)
        cls.dst = os.path.join(results, 'flatten')

        # Create destination if it does not exist
        if not os.path.isdir(cls.dst):
            os.mkdir(cls.dst)

        cls.fname = os.path.join(directory, 'document.pdf')

        cls.files = []

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("{0:15} --> {1}".format(' '.join(self.id().split('.')[-1].split('_')[1:]), t))

        # Move each file into results folder
        for i in self.files:
            source = i
            target = os.path.join(self.dst, str(os.path.basename(i)))
            shutil.move(source, target)
            self.files.remove(i)

    def test_flatten_1x(self):
        flat = Flatten(self.fname, scale=1.0, suffix='flat_1x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] / Info(flat).size[1]) <= 1)

    def test_flatten_2x(self):
        scale = 2.0
        flat = Flatten(self.fname, scale=scale, suffix='flat_2x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] * scale / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] * scale / Info(flat).size[1]) <= 1)

    def test_flatten_3x(self):
        scale = 3.0
        flat = Flatten(self.fname, scale=scale, suffix='flat_3x').save()
        self.files.append(flat)

        self.assertTrue(os.path.exists(flat))
        self.assertEqual(Info(self.fname).pages, Info(flat).pages)
        self.assertTrue(abs(Info(self.fname).size[0] * scale / Info(flat).size[0]) <= 1)
        self.assertTrue(abs(Info(self.fname).size[1] * scale / Info(flat).size[1]) <= 1)


if __name__ == '__main__':
    unittest.main()
