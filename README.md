# gcode-print

I wanted to check if a particular .stl file would fit with the physical PCBs I had on hand. I didn't really want
to spend the morning playing with calipers and CAD measuring tools, so I spent it writing a very simple-minded GCode
parser instead.

This tool generates a PDF at 1:1 scale (luckily my 3d printer build area is just less than A4 width) of parts of a gcode
file. It has been tested with Cura 2.4 output only. In fact, it has been tested with one GCode file, at this point! It
understands exactly enough gcode to draw that file, (and possibly not even that much).

So with PDF in hand, you can print in 2d, making sure that scale-to-fit is turned OFF, and use the resulting paper
print to verify dimensions, holes lining up etc, without wasting any plastic.

It uses CairoCFFI to generate the PDF file. That in turn requires the libcairo-2.dll on your path. So to get going:

    # On windows, install the GTK redist from: https://sourceforge.net/projects/gtk-win/?source=typ_redirect
    # then:
    pip install -r requirements.txt
    python gcode-print.py --input test.gcode --output test.pdf --min-z 3 --max-z 6

Z values are in mm.

Extending the parser is very simple - just add new methods to the gcode/__init__.py file named for the G-code or M-code.

MIT licensed. I can't imagine you'll use it for much of importance.


Howie

Twitter: @anotherhowie
github: howardjones