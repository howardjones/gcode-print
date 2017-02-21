# gcode-print

I wanted to check if a particular .stl file would fit with the physical PCBs I had on hand. I didn't really want
to spend the morning playing with calipers and CAD measuring tools, so I spent it writing a very simple-minded GCode
parser instead.

This tool generates a PDF at 1:1 scale (luckily my 3d printer build area is just less than A4 width) of parts of a gcode
file. It has been tested with Cura 2.4 output only. In fact, it has been tested with one GCode file, at this point!

So with PDF in hand, you can print in 2d, making sure that scale-to-fit is turned OFF, and use the resulting paper
print to verify dimensions, holes lining up etc, without wasting any plastic.

