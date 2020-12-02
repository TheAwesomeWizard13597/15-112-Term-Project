#From course notes
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

def initColors(app):
    app.lightColorPalette = {'grassColor': rgbString(124, 252, 0),
                        'backgroundUI':rgbString(84, 13, 110),
                        'buttonColor1':rgbString(238, 66, 102),
                        'buttonColor2':rgbString(255, 210, 63),
                        'buttonColor3':rgbString(59, 206, 172),
                        'textColor':rgbString(14, 173, 105)
                        }
    app.colorPalette = app.lightColorPalette