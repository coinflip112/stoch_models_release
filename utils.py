from IPython.display import Image, display


def view_pydot(pdot):
    plt = Image(pdot.create_png())
    display(plt)
