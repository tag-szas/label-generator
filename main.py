from fasthtml.common import *
# from fasthtml.common import FastHTML
from fasthtml.common import FastHTMLWithLiveReload, Group
from fasthtml.common import Title, Link, Style, FileResponse
from fasthtml.common import Form, Fieldset, Legend, Label, Input, Textarea, Button, Div, P, Br, H1, Img
import uvicorn
import qrlabel
from time import time


style = Link(rel="stylesheet", href="doodle.css")
font = Style("""@import url('https://fonts.googleapis.com/css2?family=Short+Stack&display=swap');""")
body_style = ("max-width: 700px;",
              "background-color: lavender;",
              "font-family: 'Short Stack', cursive;")
# app = FastHTML(hdrs=(style, font), style=body_style)
app = FastHTMLWithLiveReload(hdrs=(style, font), cls='doodle', style=body_style)


# Main page
@app.get("/")
def home():
    page = (
        Title('Image Generation Demo'),
        H1('Label Generator'),
        Form(Group(
            Label("Einfaches Label", _for="example-input-text"), Br(),
            Input(id="new-prompt", name="text", placeholder="Ein Tag / Name / etc...", autofocus=True, tabindex="1",
                  hx_trigger="input changed delay:100ms",
                  hx_get="/pure_label",
                  hx_target="#svg_preview",
                  hx_swap="outerHTML"), Br(),
            label_svg_preview(''), Br(),
            Button("Drucken", hx_get="/print_label?label_type=normal", hx_swap='none', tabindex="-1"))),
        Fieldset(
            Legend("QR-Label"),
            Form(
                Input(id="label", _type="label", placeholder="z.B.abc231", tabindex="2",
                      hx_trigger="input changed delay:200ms ",
                      hx_get="/qrlabel",
                      hx_target="#svg_qr_preview",
                      hx_swap="outerHTML"), Br(),
                qrlabel_svg_preview(''), Br(),
                Button('Drucken', hx_get='/print_label?label_type=qr', hx_swap="none", tabindex="-1"))),
        P(Button('Glückskeks', hx_post="/printcookie", hx_swap='none')),
        P(Button('Lob-O-Mat', hx_post="/lobomat", hx_swap='none')),
    )
    return page


# For file, i.e. images, CSS, etc.
@app.get("/{fname:path}.{ext:static}")
def static(fname: str, ext: str):
    return FileResponse(f'{fname}.{ext}')


@app.get("/pure_label")
def label_svg_preview(text: str):
    filename = 'normal_label.svg'
    qrlabel.make_label(text, filename)
    return Img(id="svg_preview", src=f"{filename}?ts={time()}", style='min-height:10em')


@app.get("/qrlabel")
def qrlabel_svg_preview(label: str):
    qrlabel.QRCode_svg(label, 'qr_label.svg')
    return Img(id="svg_qr_preview", src=f"qr_label.svg?ts={time()}", style='min-height:10em')


@app.get("/print_label")
def print_svg(label_type: str = 'output'):
    filename: str = label_type + '_label.svg'
    print(filename)
    qrlabel.print_file(filename)


@app.post("/lobomat")
def print_lob():
    qrlabel.make_cookie(fortune_list="bestaetigungen")
    qrlabel.print_file()


@app.post("/printcookie")
def print_cookie():
    qrlabel.make_cookie(fortune_list='')
    qrlabel.print_file()


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
