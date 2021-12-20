"""
Created on Dec 16, 2012

@author: daniel
"""

from collections import OrderedDict

import wx

from src.pyform.Controls import (
    Button,
    CheckBox,
    ColorPicker,
    ComboBox,
    FloatSpin,
    FontPicker,
    IpAddrCtrl,
    PassCtrl,
    RadioButton,
    Row,
    Slider,
    StaticLine,
    StaticText,
    TextCtrl,
    TreeCtrl,
)
from src.pyform.Form import Form, FormDialog


class MainDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="PyForm Demo Selections")
        self.form["Parts"] = parts = OrderedDict()
        parts["Buttons", Form.NC] = buttons = list()
        buttons.extend(
            [
                (
                    Button(name="DemoForm", label="Demo Form 1"),
                    Button(name="DemoFormGrowable", label="Expanding Demo"),
                    Button(name="DemoNested", label="Nesting Containers"),
                    Button(name="DemoNestedHorizontal", label="Side By Side"),
                    Button(name="ComplicatedDemo", label="Too Complex"),
                    Button(name="ComprehensiveDemo", label="Lots of Controls"),
                ),
                (StaticLine(proportion=1),),
                (
                    Button(name="GridDemos", label="A grid?"),
                    Button(name="DemoLeftStacked", label="Stacking Containers"),
                    Button(name="AlternateDeclaration", label="Another Way"),
                    Button(name="LineDemo", label="Static Lines"),
                    Button(name="AddButtons", label="Custom Buttons"),
                ),
            ]
        )
        super(MainDemo, self).__init__(parent, **kwargs)

    def bind(self):
        Form.bind(self)
        for name in self.elements.keys():
            self.Bind(
                wx.EVT_BUTTON,
                lambda e, f=globals()[name]: FormDialog(self, f),
                name,
            )


class DemoForm(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Demo Form 1",
            "Parts": OrderedDict(
                [
                    (
                        "Test Section",
                        [
                            StaticText(label="This is the first form in our demo."),
                            StaticText(label="It is not terribly complicated."),
                            StaticText(
                                label="Down here is a button that will let us proceed."
                            ),
                            Button(
                                label="Click Me To Proceed",
                                name="Continue",
                                proportion=0,
                            ),
                        ],
                    )
                ]
            ),
        }
        Form.__init__(self, parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.onContinue, "Continue")
        Form.bind(self)

    def onContinue(self, evt=None):
        FormDialog(self.Parent, panel=DemoFormGrowable, offset=25)


class DemoFormGrowable(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Demo with Growable Regions",
            "Parts": OrderedDict(
                [
                    (
                        ("Growable Form", Form.G),
                        [
                            StaticText(
                                label="This Box Sizer will use up available space."
                            )
                        ],
                    )
                ]
            ),
        }
        Form.__init__(self, parent, **kwargs)


class DemoNested(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Nexted Containers",
            "Parts": OrderedDict(
                [
                    (
                        ("Test Nested Growables", Form.G),
                        [
                            OrderedDict(
                                [
                                    (
                                        ("Inner Growable", Form.G),
                                        [
                                            StaticText(
                                                label="This Test is a bit less likely to work."
                                            )
                                        ],
                                    )
                                ]
                            ),
                            OrderedDict(
                                [
                                    (
                                        ("Inner Growable 2", Form.G),
                                        [
                                            StaticText(
                                                label="This Test is a bit less likely to work."
                                            )
                                        ],
                                    )
                                ]
                            ),
                        ],
                    )
                ]
            ),
        }
        Form.__init__(self, parent, **kwargs)


class DemoNestedHorizontal(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Horizontally Nested",
            "Parts": OrderedDict(
                [
                    (
                        ("Test Nested Growables", Form.G),
                        [
                            (
                                OrderedDict(
                                    [
                                        (
                                            ("Inner Growable", Form.G),
                                            [
                                                StaticText(
                                                    label="This Test is a bit less likely to work."
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                OrderedDict(
                                    [
                                        (
                                            ("Inner Growable 2", Form.G),
                                            [
                                                StaticText(
                                                    label="This Test is a bit less likely to work."
                                                )
                                            ],
                                        )
                                    ]
                                ),
                            )
                        ],
                    )
                ]
            ),
        }
        Form.__init__(self, parent, **kwargs)


class ComplicatedDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Getting More Complicated",
            "Parts": OrderedDict(
                [
                    (
                        ("Test Nested Growables", Form.G),
                        [
                            (
                                OrderedDict(
                                    [
                                        (
                                            ("Inner Growable", Form.G),
                                            [
                                                StaticText(
                                                    label="This Test is a bit less likely to work."
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                OrderedDict(
                                    [
                                        (
                                            ("Inner Growable 2", Form.G),
                                            [
                                                StaticText(
                                                    label="This Test is a bit less likely to work."
                                                )
                                            ],
                                        )
                                    ]
                                ),
                            ),
                            [
                                (
                                    StaticText(label="Inner 1"),
                                    StaticText(label="Inner 2"),
                                    OrderedDict(
                                        [
                                            (
                                                ("Inner Growable 2", Form.G),
                                                [
                                                    StaticText(
                                                        label="This Test is a bit less likely to work."
                                                    ),
                                                    (
                                                        CheckBox(
                                                            name="Check1",
                                                            label="A few samples.",
                                                        ),
                                                        StaticText(label="Like This."),
                                                    ),
                                                ],
                                            )
                                        ]
                                    ),
                                    StaticText(label="Another Inner"),
                                )
                            ],
                        ],
                    )
                ]
            ),
        }
        Form.__init__(self, parent, **kwargs)


class ComprehensiveDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = {
            "Title": "Comprehensively Complicated",
            "Parts": OrderedDict(
                [
                    (
                        "Lots Of Types of Elements",
                        [
                            # These first several are stand alone.
                            FontPicker(name="FontPicker"),
                            StaticText(label="We've seen these.  This one is unnamed."),
                            CheckBox(
                                name="Check1",
                                label="Checkboxes are fun.  This one "
                                      "controls the input below it.",
                            ),
                            TextCtrl(name="Input1"),
                            # Then several in a row
                            (
                                StaticText(label="Passwords can be accomodated."),
                                PassCtrl(name="Pass1"),
                            ),
                            Button(name="Button1", label="This is just a button."),
                            TreeCtrl(
                                name="Tree1", proportion=1
                            ),  # todo tree needs populated.
                            # Grids take place here.
                            [
                                (
                                    ComboBox(name="Combo1", choices=["1", "2", "3"]),
                                    FloatSpin(
                                        name="FloatSpin1",
                                        min_val=0,
                                        max_val=30,
                                        digits=2,
                                        increment=0.1,
                                        size=(30, -1),
                                        flags=wx.EXPAND | wx.ALL,
                                    ),
                                    StaticText(label="Ip Addresses are fairly common."),
                                    IpAddrCtrl(name="IpAddresses"),
                                ),
                                (
                                    RadioButton(name="R1", label="Radios"),
                                    RadioButton(name="R2", label="can be linked"),
                                    RadioButton(
                                        name="R3", label="Or", style=wx.RB_GROUP
                                    ),
                                    RadioButton(name="R4", label="Disconnected"),
                                ),
                            ],
                        ],
                    ),
                    (
                        ("Another Container - With Nesting (Take Care).", Form.G),
                        [
                            # Are you paying close attention here?  We're nesting OrderedDict's
                            # in tuple's to get side-by-side BoxSizers
                            (
                                OrderedDict(
                                    [
                                        (
                                            "Inner Container 1",
                                            [
                                                (
                                                    StaticText(
                                                        label="Colors Are Good."
                                                    ),
                                                    ColorPicker(name="Color1"),
                                                )
                                            ],
                                        )
                                    ]
                                ),
                                OrderedDict(
                                    [("Inner Contaner 2", [Slider(name="Slider1")])]
                                ),
                                OrderedDict(
                                    [
                                        (
                                            "Inner Contaner 3",
                                            [
                                                Slider(
                                                    name="Slider2",
                                                    minValue=1,
                                                    maxValue=100,
                                                    style=wx.SL_LABELS,
                                                )
                                            ],
                                        )
                                    ]
                                ),
                            ),
                            # Which we're going to place above another container.
                            OrderedDict(
                                [
                                    (
                                        (
                                            "This is getting kind of deeply nested.",
                                            Form.G,
                                        ),
                                        [
                                            OrderedDict(
                                                [
                                                    (
                                                        (
                                                            "But we're showing just how intricate",
                                                            Form.G,
                                                        ),
                                                        [
                                                            StaticText(
                                                                label="your forms can be."
                                                            )
                                                        ],
                                                    )
                                                ]
                                            )
                                        ],
                                    )
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        }
        super(ComprehensiveDemo, self).__init__(parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_CHECKBOX, self.onCheck1, "Check1", True)
        super(ComprehensiveDemo, self).bind()

    def onCheck1(self, evt=None):
        self.elements["Input1"].Enable(self.elements["Check1"].GetValue())


class AlternateDeclaration(Form):
    """
    This example provides a different way to declare forms, in case the
    nesting from the previous example was a bit overwhelming.
    """

    def __init__(self, parent, **kwargs):
        self.form = {"Title": "Easier to Read (?)"}
        defaults = self.form["Defaults"] = {}
        options = self.form["Options"] = {}
        parts = self.form["Parts"] = OrderedDict([])
        parts["Outermost"] = outer = list()
        outer.append(CheckBox(name="Check1", label="Just a checkbox."))
        outer.append(StaticText(label="And some text."))
        outer.append(
            (
                StaticText(label="These should form ", gap=0),
                StaticText(label="a row.", gap=0),
            )
        )
        outer.append(
            StaticText(
                label="The significance of this form lies in the Source.  You'll need to look there ... "
            )
        )
        inner = OrderedDict([])
        inner["Sub 1"] = sub1 = list()
        sub1.append(ComboBox(name="Combo", proportion=1))
        defaults["Combo"] = "Default Value"
        options["Combo"] = [str(i) for i in range(10)]
        outer.append(inner)
        super(AlternateDeclaration, self).__init__(parent, **kwargs)


class GridDemos(Form):
    def __init__(self, parent, **kwargs):
        self.form = {"Title": "Nested Grids"}
        parts = self.form["Parts"] = OrderedDict()
        for row in range(10):
            row_list = parts["Row %d" % row] = list()
            cols = list()
            for col in range(10):
                inner = OrderedDict()
                innermost = inner["Col %d" % col] = list()
                innermost.append(StaticText(label="%d x %d" % (row, col)))
                cols.append(inner)
            row_list.append(tuple(cols))
        super(GridDemos, self).__init__(parent, **kwargs)


class DemoLeftStacked(Form):
    def __init__(self, parent, **kwargs):
        self.form = {"Title": "Left Stacked Demo"}
        parts = self.form["Parts"] = OrderedDict()
        outermost = parts[("Outermost", Form.G)] = list()
        left, right = OrderedDict(), OrderedDict()
        outermost.append(Row((left, right), rowGrowable=True, proportion=1))
        l1 = left[("Left Top", Form.G)] = list()
        l1.append(StaticText(label="Left Top Inner"))
        l2 = left[("Left Bottom", Form.G)] = list()
        l2.append(StaticText(label="Left Bottom Inner"))
        r1 = right[("Right", Form.G)] = list()
        r1.append(
            TextCtrl(
                name="Text",
                style=wx.TE_MULTILINE,
                colGrowable=True,
                rowGrowable=True,
                proportion=1,
            )
        )
        super(DemoLeftStacked, self).__init__(parent, **kwargs)


class NonDialog(Form):
    def __init__(self, parent, **kwargs):
        self.form = {}
        parts = self.form["Parts"] = OrderedDict()
        main = parts[("Main", Form.G | Form.NC)] = list()
        main.append(StaticText(label="This is where you would create your app."))
        inner = OrderedDict()
        main.append(inner)
        inner[("Sub Region 1", Form.G)] = list()
        super(NonDialog, self).__init__(parent, **kwargs)


class LineDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Line Demo")
        self.form["Parts"] = parts = OrderedDict()
        parts["Container", Form.NC] = [
            (Button(label="Analyze All", proportion=1),),
            (StaticLine(proportion=1),),
            (
                Button(label="Plot FWHM", proportion=1),
                Button(label="Save Data", proportion=1),
            ),
        ]
        super(LineDemo, self).__init__(parent, **kwargs)


class AddButtons(Form):
    """
    This demonstrates how to add custom buttons to a Dialog.
    Using AddButtons will prevent the standard buttons from
    being added to the form - you'll have to add _all_ buttons
    you want to use.

    When creating buttons this way, the FormDialog will attempt
    to bind each button to a corresponding `on<Name>` method
    on your form. If you want button events, add these methods.
    """
    def __init__(self, parent, **kwargs):
        print(wx.ID_YES, wx.ID_OK)
        self.form = dict(
            Title="Custom Buttons",
            Parts=OrderedDict(Spacer=[StaticLine()]),
            AddButtons=dict(
                Save=wx.NewIdRef(1),
                Ok=wx.NewIdRef(1),
            ),
        )
        super().__init__(parent, **kwargs)


if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    MainDemo(f)
    f.Show()
    app.MainLoop()
