# PDF Watermarker

A PDF tool for adding dynamically generated watermarks to PDF documents.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to use this application you will need to have a Python 3 interpreter installed on your machine.  A limited functionality executable application has been developed for Windows 10 to bypass Python as a system dependency.

Upgrade to the latest version of pip.

```
pip install --upgrade pip
```

### Installation

Install the latest version from the PyPi distribution.  Run pip install pdfwatermarker on the command line of your interpreter (virtual environment not required but recommended).

PyPi install

```
pip install pdfwatermarker
```
PyPi update (no cache dir to force install of newest version)

```
pip install --no-cache-dir --upgrade pdfwatermarker
```

### Project Structure

```
pdfwatermarker/
├── thirdparty
│   ├── PyPDF2
│   ├── __init__.py
│   └── icon.ico
├── utils
│   ├── __init__.py
│   ├── extract.py
│   ├── info.py
│   ├── override.py
│   ├── path.py
│   ├── samples.py
│   ├── view.py
│   └── write.py
├── watermark
│   ├── draw
│   │   ├── __init__.py
│   │   ├── _objects.py
│   │   ├── canvas.py
│   │   └── image.py
│   ├── lib
│   │   ├── font
│   │   ├── img
│   │   ├── __init__.py
│   │   ├── gui.py
│   │   ├── receipt.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── add.py
│   ├── label.py
│   └── watermark.py
├── __init__.py
├── encrypt.py
├── merge.py
├── rotate.py
├── slice.py
└── upscale.py

```


## Purpose

PDFWatermarker was developed to streamline the redundant process of creating watermarks, overlaying them on PDF files and adding security parameters before distribution to clients.

#### Process "as is"
 
1. Photoshop
	* Open watermark PSD template
	* Modify text (address, town, state)
	* Save file to PNG
2. Acrobat (watermark)
	* Open source PDF file
	* Find PNG file and add as a watermark
	* Save new file with '_watermarked' suffix
3. Acrobat (security)
	* Open watermarked PDF file
	* Add user and owner password protection
	* Restrict permissions to 'Print Only'

#### Process "automated"

1. Run pdfwatermark GUI
2. Select source PDF file
3. Input text (address, town, state)
4. Select watermark and encryption parameters

By removing the steps of launching Photoshop and Acrobat to perform a number of tasks process efficiency is dramatically increaded.

## High Level APIs

Outlined below are basic uses of the main classes and functions of the PDF watermarker python package.

* WatermarkGUI - GUI for setting source file and watermark parameters
	* Launch GUI window to set source file and watermark settings
	* Dependent on PySimpleGUI library and TKinter back-end
	* Return inputs to caller
* Watermark - Wrapper class that manages inputs and file structures
	* Creates watermark file
	* Merges watermark file and source document file
	* Saves new watermark and removes temp files
* WatermarkDraw - Dynamically generates a watermark using CanvasObjects
	* Set text, image, font, opacity and location parameters by creating CanvasStr and CavnasImg objects
	* Draw to letter sized canvas
	* Add rotation to canvas for rotated watermarked
	* Merges watermark template and dynamically drawn canvas or image to create watermark
	* Write watermark pdf file to temp folder and returns path
* WatermarkAdd - Merges source PDF file with the watermark generated by WatermarkDraw
	* Checks if source PDF file is verically or horizontally oriented
	* Calls upscale() to upscale PDF to fit letter size (8.5 x 11)
	* Checks if watermark orientation is the same as source pdf file's
		* Calls rotate() function to rotate watermark by increments of 90 degrees if needed
	* Merges source PDF file and watermark file to create new PDF object
* rotate() - Rotate PDF by increments of 90 degrees
* upscale() - Upscales PDF to fit letter size
* protect() - Encrypt a PDF document to add passwords and permissions
* Merge() - Concatenate multiple PDF documents into one PDF
* slicer() - Save range of pages in PDF document to a new PDF file

## Usage - Watermark
Generate watermark, add watermark to file and encrypt file
#### Using module imports.

```python
from pdfwatermarker import Watermark

# Set document and watermark params
pdf = 'mypdfdoc.pdf'
address = '2000 Main Street'
town = 'Boston'
state = 'MA'

# Initialize with PDF document
w = Watermark(pdf)

# Generate watermark file
w.draw(text1=address, text2=town + ', ' + state, copyright=True, rotate=30, opacity=0.08

# Add watermark file to PDF document
w.add()
>>> mypdfdoc_watermarked.pdf

# Encypt PDF document
w.encrypt(user_pw='foo', owner_pw='baz') 
>>> mypdfdoc_secured.pdf

# Remove temp files and save receipt to disk
w.cleanup()
```

#### Using GUI.
```python
from pdfwatermarker import WatermarkGUI
WatermarkGUI()
```
![GUI Screenshot](https://i.imgur.com/9pMvzJj.png)

#### Optional Parameters - Watermark Settings
###### Logo Images
* References the logo images within the pdfwatermarker/watermark/lib/img directory
* Can be replaced with any png 

```python
Watermark.draw(image='Wide.png')
```

###### File Compression
* Handles compressing of PDF object components of the watermark file
* When objects are automatically compressed this parameter may have no effect

```python
Watermark.draw(compress=0)  # Uncompressed
Watermark.draw(compress=1)  # Compressed
``` 

###### Watermark Flattening
* Set to layered by default
* Method in which a watermark file is created
* Layered
	* Creates a CanvasStr object for each text layer of the watermark stored in CanvasObjects
	* Create CanvasImg object for watermark logo image file
	* Iterate CanvasObjects and draw each to canvas
	* Save canvas with text objects to layered PDF document
* Flattened
	* Draw each text layer to PIL image file instead of a canvas
	* Store one CanvasImg containing logo image file and text layers in CanvasObjects
	* Draw CanvasImg to canvas
	* Save canvas with single image layer
* Layered vs. Flattened
	* Layered allows for finer parameter tuning with more options
	* Flattened makes watermark harder to remove by merging layers

```python
Watermark.draw(flatten=False)  # Layered
Watermark.draw(flatten=True)  # Flattened
``` 

###### Watermark Placement
* Place Watermark on top of or below existing PDF document
* Overlay placement is necessary for watermarking images
* Underneath placement is often cleaner for watermarking text heavy PDF documents

```python
Watermark.add(underneath=False)  # Overlay
Watermark.add(underneath=True)  # Underneath
```

###### Opacity
* Opacity of watermark logo image and watermark text
* Adjustable from 1% to 20%
* Opacity parameter must of type float

```python
Watermark.draw(opacity=0.09)  # Set opacity to 9%
```

## Usage - Encrypt
Encrypt a PDF file to add passwords and restrict permissions.
#### Using module imports.
```python
from pdfwatermarker import protect

# Required parameters
pdf = 'mypdfdoc.pdf'
user_pw = 'baz'  # Password to open and view PDF
owner_pw = 'foo'  # Password to change security settings

# Optional parameters
encrypt_128 = True  # Encrypt using 128 bits (40 bits when False)
restrict_permission = True  # Restrict permissions to print only (all allowed when false)

# Encrypt PDF document
encrypted = encrypt(pdf, user_pw, owner_pw, encrypt_128, restrict_permission)
>>> mypdfdoc_secured.pdf
```

## Usage - Merge
Merge multiple PDF files into one concatenated PDF file.
#### Using module imports.
```python
from pdfwatermarker import Merge

# List of PDF paths
pdfs = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']

# Merge PDF files
merged = Merge(pdfs)
>>> merged.pdf
```
or

```python
from pdfwatermarker import Merge

# List of PDF paths
pdfs = ['doc1.pdf', 'doc2.pdf', 'doc3.pdf']

# Specify output file name
output = 'combined doc'

# Merge PDF files
merged = Merge(pdfs, output_name=output)
>>> combined doc.pdf
```

## Usage - Rotate
Rotate a PDF document by increments of 90 degrees.
#### Using module imports.
```python
from pdfwatermarker import rotate

pdf = 'mypdfdoc.pdf'  # PDF to-be rotated
rotate = 90  # Degress of rotation (clockwise)

# Rotate PDF file
rotated = rotate(pdf, rotate)
>>> mypdfdoc_rotated.pdf
```

## Usage - Slice
Slice a PDF document to extract a range of page.
#### Using module imports.
```python
from pdfwatermarker import slicer

# Parameters
pdf = 'mypdfdoc.pdf'
first_page = 4
last_page = 17

# Slice PDF file
sliced = slicer(pdf, first_page, last_page)
>>> mypdfdoc_sliced.pdf
```

## Usage - Label
Add a text label to the bottom left corner of each page of PDF file.
#### Using module imports.
```python
from pdfwatermarker import Label

# Parameters
pdf = 'mypdfdoc.pdf'
label = 'Document updated 7/10/18'

# Label PDF file
labeled = Label(pdf, label)
>>> mypdfdoc_labeled.pdf
```
[Original](https://i.imgur.com/4plXGHN.png)

[Labeled](https://i.imgur.com/UvEMNxy.png)

## Functionality
### Watermark()
```python
Watermark(document, remove_temps=True, open_file=True, tempdir=mkdtemp(), receipt=None, use_receipt=True)
```
Parameters | Type | Description
--- | --- | ---
document | `str ` | PDF document full path
remove_temps | `bool` | Remove temporary files after completion
open_file | `bool` | Open file after completion
tempdir | `str or function` | Temporary directory for file writing
receipt | `cls` | Use existing Receipt object if already initiated
use_receipt | `bool` | Print receipt information to console and write to file

### Watermark().draw()
```python
Watermark().draw(self, text1, text2=None, copyright=True, image=default_image,
	 rotate=30, opacity=0.08, compress=0, add=False, flatten=False)
```
Parameters | Type | Description
--- | --- | ---
text1 | `str ` | Text line 1
text2 | `str ` | Text line 2
copyright | `bool` | Draw copyright and year to canvas
image | `str` | Logo image to be used as base watermark
rotate | `int` | Degrees to rotate canvas by
opacity | `float` | Watermark opacity
compress | `bool` | Compress watermark contents (not entire PDF)
flatten | `bool` | Draw watermark with multiple layers or a single flattened layer
add | `bool` | Add watermark to original document

**Return**: Watermark file full path

### Watermark().add()
```python
Watermark().add(document=None, watermark=None, underneath=False, output=None, suffix='watermarked')
```
Parameters | Type | Description
--- | --- | ---
document | `str ` | PDF document full path
watermark | `str ` | Watermark PDF full path
underneath | `bool` | Place watermark either under or over existing PDF document
output | `str` | Output file path
suffix | `str ` | Suffix to append to existing PDF document file name

**Return**: Watermarked PDF document full path

### Watermark().encrypt()
```python
Watermark().encrypt(user_pw='', owner_pw=None, encrypt_128=True, restrict_permission=True)
```
Parameters | Type | Description
--- | --- | ---
user_pw | `str ` | User password required to open and view PDF document
owner_pw | `str ` | Owner password required to alter security settings and permissions
encrypt_128 | `bool` | Encrypt PDF document using 128 bit keys
restrict_permission | `str` | Restrict permissions to print only

**Return**: Encrypted PDF document full path

## Challenges

* A number of PDF libraries exist I was unable to find one with the functionality I was looking for.
* Simple add watermark functionality wasn't enough, I needed the ability to adjust each watermark without opening another application.
* PDF files can only be rotated by 90 degree increments so slanted text was achieved by drawing to a rotated canvas object

## Built With

* [pdfrw](https://github.com/pmaupin/pdfrw) - pdfrw is a pure Python library that reads and writes PDFs.
* [Pillow](https://python-pillow.org/) - The friendly PIL fork (Python Imaging Library) 
* [PyPDF2](https://github.com/mstamy2/PyPDF2) - A utility to read and write PDFs with Python
* [PySimpleGUI](https://github.com/MikeTheWatchGuy/PySimpleGUI) - A simple yet powerful GUI built on top of tkinter.
* [reportlab](https://bitbucket.org/rptlab/reportlab) - Allows rapid creation of rich PDF documents, and also creation of charts in a variety of bitmap and vector formats.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/mrstephenneal/databasetools/contributing.md) for details on our code of
 conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/mrstephenneal/databasetools).

## Authors

* **Stephen Neal** - *Initial work* - [pdfwatermarker](https://github.com/mrstephenneal/pdfwatermarker)
