# !/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict, defaultdict
from traceback import print_exc

import wx
from wx import EVT_MENU

from .Controls import CheckBox, RadioButton, Row, StaticText


class FormDialog(wx.Dialog):
    def __init__(
            self,
            parent,
            panel=None,
            title="Unnamed Dialog",
            modal=False,
            sizes=(-1, -1),
            offset=None,
            gap=3,
            position=None,
            **kwargs
    ):
        wx.Dialog.__init__(
            self, parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        if panel is not None:
            self.SetTitle(title)
            self.panel = panel(self, gap=gap, **kwargs)
            self.panel.SetSizeHints(*sizes)

            ds = wx.GridBagSizer(self.panel.gap, self.panel.gap)
            ds.Add(self.panel, (0, 0), (1, 1), wx.EXPAND | wx.ALL, self.panel.gap)
            ds.Add(
                wx.StaticLine(self),
                (1, 0),
                (1, 1),
                wx.EXPAND | wx.RIGHT | wx.LEFT,
                self.panel.gap,
            )

            self.bs = self.CreateButtonSizer(
                self.panel.form.get("Buttons", wx.OK | wx.CANCEL)
            )
            ds.Add(self.bs, (2, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALL, self.panel.gap)

            ds.AddGrowableCol(0)
            ds.AddGrowableRow(0)

            self.SetSizerAndFit(ds)
            if position is None:
                self.Center()
            else:
                self.SetPosition(position)

            if offset:
                newpos = map(lambda x: x + offset, self.GetPosition())
                self.SetPosition(wx.Point(*newpos))

            self.Bind(wx.EVT_BUTTON, self.panel.onOk, id=wx.ID_OK)
            self.Bind(wx.EVT_BUTTON, self.panel.onClose, id=wx.ID_CANCEL)

            for wrapper in self.panel.elements.values():
                if not isinstance(wrapper, (RadioButton, CheckBox, StaticText)):
                    wrapper.SetFocus()
                    break

            if modal:
                self.res = self.ShowModal()
            else:
                self.Show()

    def FocusNext(self):
        for child in reversed(wx.GetTopLevelWindows()[0].GetChildren()):
            if isinstance(child, FormDialog) and child is not self:
                child.Raise()
                break

        self.Destroy()


class Form(wx.Panel):
    # Flags for containers.
    D = DEFAULT_FLAGS = 0
    G = GROWABLE = 1
    NC = NO_CONTAINER = 2
    R = RIGHT_ALIGN = 4
    VC = VERTICAL_ENTER = wx.EXPAND | wx.ALL

    def __init__(
            self, parent=None, id=-1, gap=3, sizes=(-1, -1), *args
    ):  # @ReservedAssignment
        wx.Panel.__init__(self, parent, id)

        self.SetSizeHints(*sizes)
        self.gap = gap
        self.elements = OrderedDict([])
        self.ATables = defaultdict(list)

        if hasattr(self, "form"):
            # Before building verify that several required sections exist in the form
            # definition object.
            if "Defaults" not in self.form:
                self.form["Defaults"] = {}
            if "Disabled" not in self.form:
                self.form["Disabled"] = []
            if "Validators" not in self.form:
                self.form["Validators"] = {}
            if "Options" not in self.form:
                self.form["Options"] = {}

            # Allow sub classes to add their own values or defaults.
            self.loadDefaults()
            self.loadOptions()
            self.build()
            if sizes == (-1, -1):
                self.Parent.SetSize(self.Parent.GetBestVirtualSize())
            if "Title" in self.form and hasattr(parent, "SetTitle"):
                parent.SetTitle(self.form["Title"])
            self.bind()

    def __iter__(self):
        return ((k, self[k]) for k in self.elements.keys())

    def __getitem__(self, key):
        try:
            return self.h2m(key, self.elements[key].GetValue())
        except:
            return

    def __setitem__(self, key, value=""):
        try:
            return self.elements[key].SetValue(self.m2h(key, value))
        except:
            print_exc()

    def HumanToMachine(self, name, value=""):
        if "Translations" in self.form:
            if name in self.form["Translations"]:
                value = self.form["Translations"][name][1].get(value, value)
        return value

    h2m = HumanToMachine

    def MachineToHuman(self, name, value=""):
        if "Translations" in self.form:
            if name in self.form["Translations"]:
                value = self.form["Translations"][name][0].get(value, value)
        return value

    m2h = MachineToHuman

    def Bind(self, evtType, evtFunc, evtSrc, call=False, *args, **kwargs):
        """
        I rewrote Bind a little bit to simplify binding events using the names
        that you assign to individual elements.  The call signature is the
        same, and it only triggers when you pass the *wrong* type argument
        as the event source, so it shouldn't affect existing Bind calls.
        """
        if isinstance(evtSrc, str):
            evtSrc = self.elements[evtSrc]
        #    if isinstance(evtType, wx.CommandEvent):
        evtSrc.Bind(evtType, evtFunc)
        #    else:
        #      super(Form, self).Bind(evtType, evtFunc, evtSrc, *args, **kwargs)
        if call:
            evtFunc()

    def Accel(self, key, func, elem, kind=wx.ACCEL_NORMAL):
        """
        This convenience function is provided to simplify Accelerator Table
        creation.  It builds Accelerator Tables over repeated calls for
        the windows indicated by `elem`. The tables will be set in the
        bind method (the default behavior).
        """
        self.ATables[elem].append((kind, key, func))

    def build(self):
        """
        The Build Method automates sizer creation and element placement by parsing
        a properly constructed object.
        """

        # The Main Sizer for the Panel.
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        # Pass the outermost Parts and the container to the OrderedDict Parser.
        self.parseContainer(self.form["Parts"], panelSizer)
        self.SetSizerAndFit(panelSizer)

    def bind(self):
        # Attempt to accommodate non-dialog parents.
        if not isinstance(self.Parent, FormDialog):
            self.Parent.Bind(wx.EVT_CLOSE, self.onClose)
        for name, table in self.ATables.items():
            if table:
                at = []
                for kind, key, func in table:
                    at.append((kind, key, key))
                    EVT_MENU(self.elements[name], key, func)
                self.elements[name].SetAcceleratorTable(wx.AcceleratorTable(at))

    def parseContainer(self, container, outerSizer, pos=None, span=None):
        sectionSizer = wx.BoxSizer(wx.VERTICAL)
        for section in container.items():
            region, proportion = self.parseSection(section)
            sectionSizer.Add(region, proportion, flag=Form.VC, border=self.gap)
        if isinstance(outerSizer, wx.GridBagSizer):
            outerSizer.Add(
                sectionSizer, pos, span, border=self.gap, flag=wx.ALIGN_CENTER_VERTICAL
            )
            if proportion:
                row, col = pos
                outerSizer.AddGrowableRow(row)
                outerSizer.AddGrowableCol(col)
        else:
            outerSizer.Add(sectionSizer, 1, flag=Form.VC, border=self.gap)

    def parseSection(self, section):
        container, blocks = section
        if isinstance(container, tuple):
            display, flags = container
        else:
            # String instead of tuple.
            flags = Form.D
            display = container
        self.flags = flags
        sizerProportion = 1 if flags & Form.G else 0
        if flags & Form.NC:
            sectionSizer = wx.BoxSizer(wx.VERTICAL)
        else:
            box = wx.StaticBox(self, -1, display)
            sectionSizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        for block in blocks:
            self.parseBlock(block, sectionSizer)
        return sectionSizer, sizerProportion

    def parseBlock(self, block, sectionSizer):
        """
        The form structure is a list of rows (blocks) in the form.  Each row
        consists of a single element, a row of elements, or a sub-grid of
        elements.  These are represented by dictionaries, tuples, or lists,
        respectively and are each processed differently.
        """
        proportion = 0
        if isinstance(block, OrderedDict):
            return self.parseContainer(block, sectionSizer)
        if isinstance(block, list):
            item = self.makeGrid(block)
        elif isinstance(block, (tuple, Row)):
            proportion = getattr(block, "proportion", proportion)
            item = self.makeRow(block)
        else:
            proportion = block.proportion
            item = self.makeWidget(block)
        sectionSizer.Add(item, proportion, flag=Form.VC, border=self.gap)

    def makeRow(self, fields):
        """
        In the form structure a tuple signifies a row of elements.  These items
        will be arranged horizontally without dependency on other rows.  Each
        item may provide a proportion property which can cause that element to
        expand horizontally to fill space.
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        for field in fields:
            self.parseBlock(field, sizer)
        return sizer

    def makeGrid(self, rows):
        """
        In the form structure a list signifies a grid of elements (equal width
        columns, rows with similar numbers of elements, etc).
        """
        sizer = wx.GridBagSizer(0, 0)
        for row, fields in enumerate(rows):
            for col, field in enumerate(fields):
                # Each item may specify that its row or column 'grow' or expand to fill
                # the available space in the form. Spans or specific positions are also
                # possible.
                flags = getattr(field, "flags", wx.ALL)
                rowGrowable = getattr(field, "rowGrowable", False)
                colGrowable = getattr(field, "colGrowable", True)
                span = getattr(field, "span", (1, 1))
                pos = (
                    getattr(field, "rowpos", row) or row,
                    getattr(field, "colpos", col) or col,
                )
                if isinstance(field, OrderedDict):
                    self.parseContainer(field, sizer, pos, span)
                else:
                    element = self.makeWidget(field)
                    sizer.Add(
                        element,
                        pos,
                        span,
                        border=self.gap,
                        flag=wx.ALIGN_CENTER_VERTICAL | flags,
                    )
                if (
                        rowGrowable
                        and row < sizer.GetRows()
                        and not sizer.IsRowGrowable(row)
                ):
                    sizer.AddGrowableRow(row)
                if (
                        colGrowable
                        and col < sizer.GetCols()
                        and not sizer.IsColGrowable(col)
                ):
                    sizer.AddGrowableCol(col)
        return sizer

    def makeWidget(self, declarator):
        """
        This function actually creates the widgets that make up the form.
        Each element should provide a `make` method which takes as an argument
        it's parent, and returns a wx item (sizer, form element, etc).
        Other methods for each widget (defined with placeholders on
        the wxPlaceholder Class) are
          GetValue
          SetValue
          SetValidator
          SetOptions
        """

        # Attach the elements container to the declarator.
        declarator._elements = self.elements
        element = declarator.make(self)
        if declarator.name:
            self.elements[declarator.name] = declarator
            # Disable if requested.
            if declarator.name in self.form["Disabled"]:
                declarator.Enable(False)
            # Options need to exist early.
            if hasattr(declarator, "SetOptions"):
                declarator.SetOptions(self.form["Options"].get(declarator.name, []))
            # We need to use the existing value if there isn't one in defaults
            # to prevent StaticText's from ending up blank.
            value = self.form["Defaults"].get(declarator.name, declarator.GetValue())
            # Assign or populate any fields requiring it.
            declarator.SetValue(self.m2h(declarator.name, value))
            declarator.SetValidator(self.form["Validators"].get(declarator.name, None))
        return element

    def loadDefaults(self):
        pass

    def loadOptions(self):
        pass

    def onOk(self, evt):
        evt.Skip()
        self.onClose(evt)

    def onClose(self, evt):
        evt.Skip()
        if isinstance(self.Parent, FormDialog):
            self.Parent.FocusNext()

    def fieldValidate(self):
        if "Validators" not in self.form:
            return True
        success, messages = True, []
        for name, field in self.elements.items():
            if name in self.form["Validators"]:
                s, m = field.Validate()
                if not s:
                    success = False
                    messages.extend(m)
        if messages:
            text = "\r\n".join(messages)
            wx.MessageDialog(self, text, "Form Field Error", wx.OK).ShowModal()
        return success


if __name__ == "__main__":
    from src.pyform.Demos import (
        DemoForm,
        DemoFormGrowable,
        DemoNested,
        DemoNestedHorizontal,
        ComplicatedDemo,
        ComprehensiveDemo,
        AlternateDeclaration,
        GridDemos,
        DemoLeftStacked,
        NonDialog,
    )

    app = wx.PySimpleApp()
    f = wx.Frame(None)
    NonDialog(f)
    f.Show()
    FormDialog(parent=f, panel=DemoForm)
    FormDialog(parent=f, panel=DemoFormGrowable)
    FormDialog(parent=f, panel=DemoNested)
    FormDialog(parent=f, panel=DemoNestedHorizontal)
    FormDialog(parent=f, panel=ComplicatedDemo)
    FormDialog(parent=f, panel=ComprehensiveDemo)
    FormDialog(parent=f, panel=AlternateDeclaration)
    FormDialog(parent=f, panel=GridDemos)
    FormDialog(parent=f, panel=DemoLeftStacked, gap=1)

    app.MainLoop()
