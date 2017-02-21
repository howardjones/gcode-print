import cairocffi as cairo

from collections import Counter


class GCodeFile(object):
    POINTS_PER_MM = 0.352778
    MM_PER_POINT = 1.0 / 0.352778

    def __init__(self, filename):
        self.mode = "rel"
        self.filename = filename
        self.units = "mm"
        self.x = 0
        self.y = 0
        self.z = 0

        self.min_z = 3
        self.max_z = 6

        self.layer_lines = 0

        self.surface = cairo.PDFSurface("test2.pdf", 1440, 1440)
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

        print(counters)
        print("Final: {0},{1},{2}".format(self.x, self.y, self.z))

    def write_pdf(self):
        pass

    def line(self, x0, y0, x1, y1):
        self.context.move_to(x0 * self.MM_PER_POINT, y0 * self.MM_PER_POINT)
        self.context.line_to(x1 * self.MM_PER_POINT, y1 * self.MM_PER_POINT)
        self.context.stroke()

    def G0(self, args):
        """move rapids"""
        self.G1(args)

    def G1(self, args):
        """move straight line"""
        # print("bzzz ")

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
            print("UP to {1}! {0} lines in last layer [{2}]".format(self.layer_lines, new_z, self.mode))
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
