from gcode import GCodeFile

g = GCodeFile("test.gcode")
g.read_file()
g.write_pdf()
