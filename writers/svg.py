from util.mathutil import BoundingBox, Line

color = 'blue'

header_template = '''
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="%(width_in)f%(units)s" height="%(height_in)f%(units)s" \
viewBox="0 0 %(width)f %(height)f" xmlns="http://www.w3.org/2000/svg" version="1.1">
    <title>F-engrave Output</title>
    <desc>SVG File Created By F-Engrave</desc>'''

path_template = '<path d="M %f %f L %f %f" fill="none" stroke="' + color + '" ' + \
    'stroke-width="%f" stroke-linecap="round" stroke-linejoin="round" />'

circle_template = '<circle cx="%f" cy="%f" r="%f" fill="none" stroke="' + color + '" stroke-width="%f" />'


def svg(app):
    if app.cut_type.get() == "v-carve":
        thickness = 0.001
    else:
        thickness = float(app.STHICK.get())

    dpi = 100

    bbox = BoundingBox()
    for line in app.coords:
        bbox.extend(Line(line[0:4]))

    # XOrigin, YOrigin = app.get_origin()
    # Radius_plot=  float(app.RADIUS_PLOT)
    # if Radius_plot != 0:
    #     maxx = max(maxx, XOrigin + Radius_plot - app.Xzero)
    #     minx = min(minx, XOrigin - Radius_plot - app.Xzero)
    #     miny = min(miny, YOrigin - Radius_plot - app.Yzero)
    #     maxy = max(maxy, YOrigin + Radius_plot - app.Yzero)

    bbox.pad(thickness / 2)
    width_in  = bbox.xmax - bbox.xmin
    height_in = bbox.ymax - bbox.ymin

    width  = width_in * dpi
    height = height_in * dpi

    svgcode = []
    svgcode.append(header_template % {
        'width_in': width_in,
        'height_in': height_in,
        'units': app.units.get(),
        'width': width,
        'height': height
    })

    # # Make Circle
    # if Radius_plot != 0 and app.cut_type.get() == "engrave":
    #     svgcode.append('    <circle cx="%f" cy="%f" r="%f" fill="none" stroke="blue" stroke-width="%f" />' % (
    #                 ( XOrigin - app.Xzero - minx) * dpi,
    #                 (-YOrigin + app.Yzero + maxy) * dpi,
    #                   Radius_plot               ) * dpi,
    #                   thickness                   * dpi)
    # # End Circle

    for l in app.coords:
        # translate
        line = [
            l[0] - bbox.xmin, -l[1] + bbox.ymax,
            l[2] - bbox.xmin, -l[1] + bbox.ymax
        ]
        # scale
        line = map(lambda x: x * dpi, line)

        svgcode.append(path_template % (tuple(line) + (thickness * dpi, )))

    svgcode.append('</svg>')

    return svgcode
