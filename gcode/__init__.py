import cairocffi as cairo
import argparse

from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCodeFile(object):
    POINTS_PER_MM = 0.352778
    MM_PER_POINT = 1.0 / 0.352778

    def __init__(self, input_file, output_file, min_z, max_z):
        self.mode = "rel"
        self.filename = input_file
        self.units = "mm"
        self.x = 0
        self.y = 0
        self.z = 0

        self.min_z = min_z
        self.max_z = max_z

        self.layer_lines = 0

        self.surface = cairo.PDFSurface(output_file, 1440, 1440)
        self.context = cairo.Context(self.surface)
        self.context.set_source_rgb(1, 1, 1)  # White
        self.context.paint()
        self.context.set_source_rgb(0, 0, 0)
        self.context.set_line_width(0.1)

    def read_file(self):

        counters = Counter()

        with open(self.filename) as f:
            for line in f:
                line = line.strip()
                if not line.startswith(";"):
                    line = line.split(";", 1)[0].strip()
                    parts = line.split(" ")
                    command = parts[0]
                    counters[command] += 1

                    if command.startswith('G') or command.startswith('M'):
                        if command not in dir(self):
                            raise NotImplementedError("Unimplemented Gcode: " + command)
                        handler = getattr(self, command)
                        handler(parts[1:])

        logger.debug("Seen commands: %s", counters)
        logger.debug("Final position: {0},{1},{2}".format(self.x, self.y, self.z))

    def line(self, x0, y0, x1, y1):
        self.context.move_to(x0 * self.MM_PER_POINT, y0 * self.MM_PER_POINT)
        self.context.line_to(x1 * self.MM_PER_POINT, y1 * self.MM_PER_POINT)
        self.context.stroke()

    def G0(self, args):
        """move rapids"""
        self.G1(args)

    def G1(self, args):
        """move straight line"""

        new_pos = [None, None, None, None]
        new_x = self.x
        new_y = self.y
        new_z = self.z

        for arg in args:
            if arg.startswith("X"):
                new_pos[0] = float(arg[1:])
            if arg.startswith("Y"):
                new_pos[1] = float(arg[1:])
            if arg.startswith("Z"):
                new_pos[2] = float(arg[1:])
            if arg.startswith("E"):
                new_pos[3] = float(arg[1:])

        if new_pos[2]:
            new_z = new_pos[2]
            if self.mode == 'rel':
                new_z += self.z

        if new_pos[0]:
            new_x = new_pos[0]
            if self.mode == 'rel':
                new_x += self.x

        if new_pos[1]:
            new_y = new_pos[1]
            if self.mode == 'rel':
                new_y += self.y

        # only draw if the extruder was running (and running forwards!)

        # if self.min_z <= self.z <= self.max_z:
        # if new_e > 0 and self.min_z <= self.z <= self.max_z:
        if new_pos[3] and new_pos[3] > 0:
            if self.min_z <= self.z <= self.max_z:
                self.layer_lines += 1
                self.line(self.x, self.y, new_x, new_y)

        if self.z != new_z:
            logger.debug("UP to {1}! {0} lines drawn in last layer [{2} mode]".format(self.layer_lines, new_z, self.mode))
            self.layer_lines = 0

        self.x = new_x
        self.y = new_y
        self.z = new_z

    def G20(self, args):
        """Set inches"""
        self.units = "inches"

    def G21(self, args):
        """Set mm"""
        self.units = "mm"

    def G28(self, args):
        """home"""
        pass

    def G90(self, args):
        """set abs coords"""
        self.mode = "abs"

    def G91(self, args):
        """set relative coords"""
        self.mode = "rel"

    def G92(self, args):
        """reset position to 0"""
        self.x = 0
        self.y = 0
        self.z = 0

    def M82(self, args):
        """extruder absolute mode"""
        pass

    def M83(self, args):
        """extruder relative mode"""
        pass

    def M84(self, args):
        """motors off. nothing to do here"""
        pass

    def M104(self, args):
        """set extruder temperature"""
        pass

    def M106(self, args):
        """fan on"""
        pass

    def M107(self, args):
        """fan off"""
        pass

    def M109(self, args):
        """set extruder temperature and wait"""
        pass

    def M117(self, args):
        """Print to display. Nothing to do here"""
        pass

    def M140(self, args):
        """Print to display. Nothing to do here"""
        pass

    def M190(self, args):
        """Print to display. Nothing to do here"""
        pass


def main():
    parser = argparse.ArgumentParser(description='Read a gcode file, and draw it 1:1 scale to a PDF')
    parser.add_argument('--input', type=str, help='GCode file to read')
    parser.add_argument('--output', type=str, default="output.pdf", help="PDF file to create")
    parser.add_argument('--min-z', type=float, default=0, help='Lowest z-layer to draw (mm)')
    parser.add_argument('--max-z', type=float, default=9999, help="Highest z-layer to draw (mm)")
    parser.add_argument('--debug', dest="debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    g = GCodeFile(args.input, args.output, args.min_z, args.max_z)
    g.read_file()
    print("Done.")