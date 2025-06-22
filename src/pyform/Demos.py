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
        self.form = dict(Title="Demo Form 1")
        self.form["Parts"] = parts = OrderedDict()

        # Set up the main section with descriptive text and a button
        parts["Test Section"] = [
            StaticText(label="This is the first form in our demo."),
            StaticText(label="It is not terribly complicated."),
            StaticText(label="Down here is a button that will let us proceed."),
            Button(
                label="Click Me To Proceed",
                name="Continue",
                proportion=0,
            ),
        ]

        Form.__init__(self, parent, **kwargs)

    def bind(self):
        self.Bind(wx.EVT_BUTTON, self.onContinue, "Continue")
        Form.bind(self)

    def onContinue(self, evt=None):
        FormDialog(self.Parent, panel=DemoFormGrowable, offset=25)


class DemoFormGrowable(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Demo with Growable Regions")
        self.form["Parts"] = parts = OrderedDict()

        # Create a growable section that will expand to fill available space
        growable = parts[("Growable Form", Form.G)] = [
            StaticText(label="This Box Sizer will use up available space.")
        ]

        Form.__init__(self, parent, **kwargs)


class DemoNested(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Nested Containers")
        self.form["Parts"] = parts = OrderedDict()
        main_container = parts[("Test Nested Growables", Form.G)] = []

        # Create first inner container with StaticText
        inner1 = OrderedDict()
        inner1[("Inner Growable", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        # Create second inner container with StaticText
        inner2 = OrderedDict()
        inner2[("Inner Growable 2", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        # Add both inner containers to the main container
        main_container.append(inner1)
        main_container.append(inner2)

        Form.__init__(self, parent, **kwargs)


class DemoNestedHorizontal(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Horizontally Nested")
        self.form["Parts"] = parts = OrderedDict()
        main_container = parts[("Test Nested Growables", Form.G)] = []

        # Create left container
        left = OrderedDict()
        left[("Inner Growable", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        # Create right container
        right = OrderedDict()
        right[("Inner Growable 2", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        # Place containers side by side using tuple
        main_container.append((left, right))

        Form.__init__(self, parent, **kwargs)


class ComplicatedDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Less Complicated")
        self.form["Parts"] = parts = OrderedDict()
        main_container = parts[("Test Nested Growables", Form.G)] = []

        # Create top section with side-by-side containers
        left = OrderedDict()
        left[("Inner Growable", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        right = OrderedDict()
        right[("Inner Growable 2", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work.")
        ]

        # Add horizontal pair to main container
        main_container.append((left, right))

        # Create inner container for bottom section
        inner_container = OrderedDict()
        inner_container[("Inner Growable 2", Form.G)] = [
            StaticText(label="This Test is a bit less likely to work."),
            (
                CheckBox(name="Check1", label="A few samples."),
                StaticText(label="Like This."),
            ),
        ]

        # Create row of elements with the inner container
        row = (
            StaticText(label="Inner 1"),
            StaticText(label="Inner 2"),
            inner_container,
            StaticText(label="Another Inner"),
        )

        # Add row to main container
        main_container.append([row])

        Form.__init__(self, parent, **kwargs)


class ComprehensiveDemo(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="All Controls Demo")
        self.form["Parts"] = parts = OrderedDict()

        # First section with basic controls
        basic_controls = parts["Controls Section"] = [
            # Basic standalone controls
            FontPicker(name="FontPicker"),
            StaticText(label="We've seen these. This one is unnamed."),
            CheckBox(
                name="Check1",
                label="Checkboxes are fun. This one controls the input below it.",
            ),
            TextCtrl(name="Input1"),
            # Row of password controls
            (
                StaticText(label="Passwords can be accommodated."),
                PassCtrl(name="Pass1"),
            ),
            Button(name="Button1", label="This is just a button."),
            TreeCtrl(name="Tree1", proportion=1),  # todo tree needs populated.
            # Grid layout
            [
                # First row of grid
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
                    StaticText(label="IP Addresses are fairly common."),
                    IpAddrCtrl(name="IpAddresses"),
                ),
                # Second row of grid
                (
                    RadioButton(name="R1", label="Radios"),
                    RadioButton(name="R2", label="can be linked"),
                    RadioButton(name="R3", label="Or", style=wx.RB_GROUP),
                    RadioButton(name="R4", label="Disconnected"),
                ),
            ],
        ]

        # Second section with nested containers
        nested_section = parts[("Advanced Layout", Form.G)] = []

        # Three containers side by side
        container1 = OrderedDict()
        container1["Inner Container 1"] = [
            (
                StaticText(label="Colors Are Good."),
                ColorPicker(name="Color1"),
            )
        ]

        container2 = OrderedDict()
        container2["Inner Container 2"] = [Slider(name="Slider1")]

        container3 = OrderedDict()
        container3["Inner Container 3"] = [
            Slider(
                name="Slider2",
                minValue=1,
                maxValue=100,
                style=wx.SL_LABELS,
            )
        ]

        # Add horizontal row of containers
        nested_section.append((container1, container2, container3))

        # Deep nested container
        outer_container = OrderedDict()
        inner_container = OrderedDict()

        inner_container[("But we're showing just how intricate", Form.G)] = [
            StaticText(label="your forms can be.")
        ]

        outer_container[("This is getting kind of deeply nested.", Form.G)] = [
            inner_container
        ]

        # Add the deeply nested container
        nested_section.append(outer_container)

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
        self.form = dict(Title="Grid Layout Demo")
        self.form["Parts"] = parts = OrderedDict()

        # Create a smaller, more manageable grid (5x5 instead of 10x10)
        for row in range(5):
            row_section = parts[f"Row {row}"] = []
            col_containers = []

            # Create columns for this row
            for col in range(5):
                col_container = OrderedDict()
                col_content = col_container[f"Col {col}"] = []
                col_content.append(StaticText(label=f"{row} x {col}"))
                col_containers.append(col_container)

            # Add all columns as a tuple to create a row
            row_section.append(tuple(col_containers))

        super(GridDemos, self).__init__(parent, **kwargs)


class DemoLeftStacked(Form):
    def __init__(self, parent, **kwargs):
        self.form = dict(Title="Left Stacked Layout")
        self.form["Parts"] = parts = OrderedDict()
        main_container = parts[("Main Layout", Form.G)] = []

        # Create left section with top and bottom parts
        left_section = OrderedDict()
        left_top = left_section[("Left Top", Form.G)] = []
        left_top.append(StaticText(label="Left Top Inner"))

        left_bottom = left_section[("Left Bottom", Form.G)] = []
        left_bottom.append(StaticText(label="Left Bottom Inner"))

        # Create right section
        right_section = OrderedDict()
        right_content = right_section[("Right Panel", Form.G)] = []
        right_content.append(
            TextCtrl(
                name="Text",
                style=wx.TE_MULTILINE,
                colGrowable=True,
                rowGrowable=True,
                proportion=1,
            )
        )

        # Add left and right sections as a row
        main_container.append(
            Row((left_section, right_section), rowGrowable=True, proportion=1)
        )

        super(DemoLeftStacked, self).__init__(parent, **kwargs)


class NonDialog(Form):
    def __init__(self, parent, **kwargs):
        self.form = {}
        self.form["Parts"] = parts = OrderedDict()

        # Main application area
        main_area = parts[("Main Application Area", Form.G | Form.NC)] = []
        main_area.append(StaticText(label="This is where you would create your app."))

        # Create a sub-region
        sub_region = OrderedDict()
        sub_region[("Sub Region 1", Form.G)] = []

        # Add sub-region to main area
        main_area.append(sub_region)

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
