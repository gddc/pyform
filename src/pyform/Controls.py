"""
Created on Nov 9, 2011

@author: daniel

This module contains custom classes to provide functionality from
the wx module in specific ways.
"""

import json
from collections import OrderedDict
from itertools import product

import wx
from wx.adv import DatePickerCtrl as DatePickerCtrl_
from wx.aui import AuiNotebook
from wx.grid import Grid as Grid_
from wx.lib.agw.customtreectrl import CustomTreeCtrl as CustomTreeCtrl_
from wx.lib.agw.floatspin import FloatSpin as FloatSpin_
from wx.lib.agw.hyperlink import HyperLinkCtrl as HyperLinkCtrl_
from wx.lib.combotreebox import MSWComboTreeBox
from wx.lib.masked.ipaddrctrl import IpAddrCtrl as IpAddrCtrl_
from wx.lib.masked.numctrl import NumCtrl as NumCtrl_
from wx.lib.scrolledpanel import ScrolledPanel as ScrolledPanel_
from wx.py.crust import Shell

from .util.FlowSizer import FlowSizer


# from wx.lib.combotreebox import ComboTreeBox as _ComboTreeBox
class _CustomFontCtrl(wx.Button):
    """
    This custom font control class provides a Font Dialog that displays with
    EnableEffects set to False.  This is used in place of the built-in
    FontPickerCtrl which does not allow for the disabling of features
    that are currently not supported.
    """

    def __init__(self, *args, **kwargs):
        super(_CustomFontCtrl, self).__init__(*args, **kwargs)
        self.font = wx.Font(
            8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL
        )
        self.Bind(wx.EVT_BUTTON, self.onClick)

    def onEnumFonts(self, data):
        self.installed = data["font-names"]

    def onClick(self, event):
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        fontData.SetInitialFont(self.font)
        dialog = wx.FontDialog(self, fontData)
        if wx.ID_OK == dialog.ShowModal():
            fontData = dialog.GetFontData()
            self.font = fontData.GetChosenFont()
            self.__updateButton()

    def __updateButton(self):
        self.SetLabel(
            ", ".join(map(str, (self.font.GetFaceName(), self.font.GetPointSize())))
        )
        self.SetFont(self.font)

    def GetSelectedFont(self):
        return self.font

    def SetFontFromDesc(self, desc):
        self.font.SetNativeFontInfoUserDesc(desc)
        self.SetLabel(
            ", ".join(map(str, (self.font.GetFaceName(), self.font.GetPointSize())))
        )
        self.SetFont(self.font)


class Row(object):
    """
    The Row Class is provided as a utility class.  It allows you to
    provide additional keyword arguments that become attributes to
    pass to the containing Sizer. It is supplementary to the use of
    tuples in the main Form Structure.
    """

    def __init__(self, items, **kwargs):
        if not isinstance(items, tuple):
            raise TypeError("Expected a tuple for argument 'items'.")
        self.items = items
        self.name = kwargs.pop("name", None)
        self.proportion = kwargs.pop("proportion", 0)
        self.flags = kwargs.pop("flags", wx.ALL)
        self.rowGrowable = kwargs.pop("rowGrowable", False)
        self.colGrowable = kwargs.pop("colGrowable", False)
        self.span = kwargs.pop("span", (1, 1))
        self.size = kwargs.get("size", (-1, -1))
        self.rowpos = kwargs.pop("rowpos", None)
        self.colpos = kwargs.pop("colpos", None)
        self.expand = kwargs.pop("expand", True)
        self.kwargs = kwargs

    def __iter__(self):
        return iter(self.items)


class wxPlaceHolder(object):
    def __init__(self, **kwargs):
        # To facilitate advanced forms, declarators will end up with access
        # to the Form's element list.
        self._elements = None
        # Pull anything that doesn't belong to the actual element out of the
        # kwargs for use when adding to the sizer, etc.
        self.name = kwargs.get("name", None)
        self.proportion = kwargs.pop("proportion", 0)
        self.flags = kwargs.pop("flags", wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.rowGrowable = kwargs.pop("rowGrowable", False)
        self.colGrowable = kwargs.pop("colGrowable", False)
        self.border = kwargs.pop("border", 0)
        self.span = kwargs.pop("span", (1, 1))
        self.size = kwargs.get("size", (-1, -1))
        self.rowpos = kwargs.pop("rowpos", None)
        self.colpos = kwargs.pop("colpos", None)
        self.expand = kwargs.pop("expand", True)
        self.local = kwargs.pop("local", False)
        self.admin = kwargs.pop("admin", False)
        self.gap = kwargs.pop("gap", None)
        self.maxlength = kwargs.pop("maxlength", None)
        self.kwargs = kwargs

    def Validate(self):
        if hasattr(self, "validator") and self.validator:
            return self.validator().Validate(self)
        return True, []

    def SetValidator(self, validator):
        self.validator = validator


class ScrolledPanel(wxPlaceHolder, ScrolledPanel_):
    def make(self, parent):
        ScrolledPanel_.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        return None

    def SetValue(self, val):
        pass


class Panel(wxPlaceHolder, wx.Panel):
    def make(self, parent):
        wx.Panel.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        return None

    def SetValue(self, val):
        pass


class FontPicker(wxPlaceHolder, _CustomFontCtrl):
    def make(self, parent):
        _CustomFontCtrl.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        return self.GetSelectedFont().GetNativeFontInfoDesc()

    def SetValue(self, val):
        self.SetFontFromDesc(val)


class StaticLine(wxPlaceHolder, wx.StaticLine):
    def make(self, parent):
        wx.StaticLine.__init__(self, parent, **self.kwargs)
        return self


class ListBox(wxPlaceHolder, wx.ListBox):
    def make(self, parent):
        wx.ListBox.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        return self.GetStringSelection()

    def SetValue(self, val):
        self.SetStringSelection(val)


class StaticText(wxPlaceHolder, wx.StaticText):
    def make(self, parent):  # @ReservedAssignment
        bold = self.kwargs.pop("bold", False)
        size = self.kwargs.pop("fontsize", None)
        wx.StaticText.__init__(self, parent, **self.kwargs)
        font = self.GetFont()
        if size is not None:
            font.SetPointSize(size)
        if bold:
            font.SetWeight(wx.BOLD)
        self.SetFont(font)

        return self

    def SetValue(self, val):
        self.SetLabel(val)

    def GetValue(self):
        return self.GetLabel()

    def SetBackgroundColor(self, *args, **kwargs):
        return self.SetBackgroundColour(*args, **kwargs)


class Grid(wxPlaceHolder, Grid_):
    def __init__(self, *args, **kwargs):
        self._selected = None
        wxPlaceHolder.__init__(self, *args, **kwargs)

    def make(self, parent):
        Grid_.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        pass

    def SetValue(self, val):
        pass

    def GetSelectedCells(self, *args, **kwargs):
        cells = []
        topleft = self.GetSelectionBlockTopLeft()
        if topleft:
            bottomright = self.GetSelectionBlockBottomRight()
            cells.extend(self.CellsByCorners(topleft, bottomright))
        cells.extend(super(Grid, self).GetSelectedCells())
        if not cells:
            cells.extend([self.GetGridCursorPos()])
        return cells

    def GetGridCursorPos(self):
        return self.GetGridCursorRow(), self.GetGridCursorCol()

    def CellsByCorners(self, toplefts, bottomrights):
        cells = []
        for (rowstart, colstart), (rowend, colend) in zip(toplefts, bottomrights):
            cells.extend(
                product(range(rowstart, rowend + 1), range(colstart, colend + 1))
            )
        return cells


class ListCtrl(wxPlaceHolder, wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        self._selected = None
        wxPlaceHolder.__init__(self, *args, **kwargs)

    def make(self, parent):
        wx.ListCtrl.__init__(self, parent, **self.kwargs)
        return self

    def Select(self, idx, **kwargs):
        self._selected = idx
        return super(ListCtrl, self).Select(idx)

    def GetSelection(self):
        return self._selected

    def GetTextSelection(self):
        return self.GetItemText(self._selected)

    def GetValue(self):
        pass

    def SetValue(self, val):
        pass


class CheckListBox(wxPlaceHolder, wx.CheckListBox):
    def __init__(self, *args, **kwargs):
        wxPlaceHolder.__init__(self, *args, **kwargs)

    def make(self, parent):
        wx.CheckListBox.__init__(self, parent, **self.kwargs)
        return self

    def GetValue(self):
        return self.GetCheckedStrings()

    def SetValue(self, val):
        self.SetCheckedStrings(val)


class TextFlow(wxPlaceHolder):
    def make(self, parent):
        bold = self.kwargs.pop("bold", False)
        size = self.kwargs.pop("fontsize", None)
        self.element = FlowSizer()
        self.words = []
        for word in self.kwargs["label"].split():
            text = wx.StaticText(parent, label=word)
            if size or bold:
                font = text.GetFont()
                if size is not None:
                    font.SetPointSize(size)
                if bold:
                    font.SetWeight(wx.BOLD)
                text.SetFont(font)
            self.words.append(text)
            self.element.Add(text, flag=wx.TOP | wx.RIGHT, border=2)
        return self.element

    def SetValue(self, val):
        pass

    def GetValue(self):
        return " ".join(word.GetLabel() for word in self.words)


class Notebook(wxPlaceHolder, AuiNotebook):
    def make(self, parent):
        # pull pages.
        self._pdict = self.kwargs.pop("pages", OrderedDict())
        self.pages = dict()
        # No name kwarg to Notebooks.
        self.name = self.kwargs.pop("name")
        AuiNotebook.__init__(self, parent, **self.kwargs)
        # This is shady, but if it works.
        from src.pyform.Form import Form

        for tabname, contents in self._pdict.items():

            class temp(Form):
                def __init__(self, parent):
                    self.form = dict()
                    parts = self.form["Parts"] = OrderedDict()
                    parts[tabname] = contents
                    super(temp, self).__init__(parent, gap=1)

            # panel = wx.Panel(self)
            page = temp(self)
            if isinstance(tabname, tuple):
                tabname = tabname[0]
            self.AddPage(page, tabname)
            self.pages[tabname] = page
        return self

    def GetValue(self):
        pass

    def SetValue(self, val):
        pass


class CheckBox(wxPlaceHolder, wx.CheckBox):
    def make(self, parent):  # @ReservedAssignment
        wx.CheckBox.__init__(self, parent, **self.kwargs)
        return self


class TextCtrl(wxPlaceHolder, wx.TextCtrl):
    def make(self, parent):  # @ReservedAssignment
        wx.TextCtrl.__init__(self, parent, **self.kwargs)
        if self.maxlength:
            self.SetMaxLength(self.maxlength)
        return self

    def SetBackgroundColor(self, color):
        return self.SetBackgroundColour(color)


class PassCtrl(TextCtrl):
    def make(self, parent):
        if "style" in self.kwargs:
            self.kwargs["style"] |= wx.TE_PASSWORD
        else:
            self.kwargs["style"] = wx.TE_PASSWORD
        return super(PassCtrl, self).make(parent)


class Button(wxPlaceHolder, wx.Button):
    def make(self, parent):  # @ReservedAssignment
        wx.Button.__init__(self, parent, **self.kwargs)
        return self

    def SetValue(self, val):
        pass

    def GetValue(self):
        pass


class ListHolder(wxPlaceHolder):
    def make(self, parent):  # @ReservedAssignment
        self.element = self.kwargs["list"](parent, **self.kwargs)
        return self.element

    def SetValue(self, val):
        pass

    def GetValue(self):
        return self.element.GetValue()


class FolderBrowser(wxPlaceHolder, wx.DirPickerCtrl):
    def make(self, parent):  # @ReservedAssignment
        wx.DirPickerCtrl.__init__(self, parent, **self.kwargs)
        self.GetTextCtrl().SetEditable(False)
        return self

    def SetFocus(self):
        super(FolderBrowser, self).SetFocus()

    def ParentBind(self, parent, evtType, evtFunc, *args, **kwargs):
        wx.Panel.Bind(parent, wx.EVT_DIRPICKER_CHANGED, evtFunc, self.element)

    def SetValue(self, val):
        return self.SetPath(val)

    def GetValue(self):
        return self.GetPath()


class FileBrowser(wxPlaceHolder, wx.FilePickerCtrl):
    def make(self, parent):
        wx.FilePickerCtrl.__init__(self, parent, **self.kwargs)
        self.GetTextCtrl().SetEditable(False)
        return self

    def SetValue(self, val):
        return self.SetPath(val)

    def GetValue(self):
        val = self.GetPath()
        try:
            val = WNetGetUniversalName(val)
        except:
            pass
        return val


class TreeCtrl(wxPlaceHolder, wx.TreeCtrl):
    def make(self, parent):
        wx.TreeCtrl.__init__(self, parent, **self.kwargs)
        return self

    def SetValue(self, val):
        pass

    def GetValue(self, selection=None):
        if self.GetWindowStyle() & wx.TR_MULTIPLE:
            return
        if selection is None:
            pieces = []
            item = self.GetSelection()
            if not item:
                return None
            while self.GetItemParent(item):
                piece = self.GetItemText(item)
                pieces.insert(0, self.parent.netcache.get(piece, piece))
                item = self.GetItemParent(item)
            if pieces[1:]:
                return "\\".join(pieces[1:])
            else:
                return None
        return self.element.GetItemText(selection)


class ComboBox(wxPlaceHolder, wx.ComboBox):
    def make(self, parent):
        wx.ComboBox.__init__(self, parent, **self.kwargs)
        return self

    def GetId(self):
        return wx.ComboBox.GetId(self)

    def SetOptions(self, options):
        self.Clear()
        self.AppendItems(options)

    def SetBackgroundColor(self, color):
        return self.SetBackgroundColour(color)


class SpinCtrl(wxPlaceHolder, wx.SpinCtrl):
    def make(self, parent):
        wx.SpinCtrl.__init__(self, parent, **self.kwargs)
        return self


class RadioButton(wxPlaceHolder, wx.RadioButton):
    def make(self, parent):
        wx.RadioButton.__init__(self, parent, **self.kwargs)
        return self


class StaticBitmap(wxPlaceHolder):
    def make(self, parent):
        self.element = wx.StaticBitmap(parent, **self.kwargs)
        return self.element

    def SetValue(self, val):
        pass

    def GetValue(self):
        pass

    def SetBitmap(self, val):
        return self.element.SetBitmap(val)


class ColorPicker(wxPlaceHolder):
    def make(self, parent):
        self.element = wx.ColourPickerCtrl(parent, **self.kwargs)
        return self.element

    def SetValue(self, val):
        self.element.SetColour(wx.Colour(**json.loads(val)))

    def GetValue(self):
        color = self.element.GetColour()
        return json.dumps(
            {"red": color.Red(), "green": color.Green(), "blue": color.Blue()}
        )


class Slider(wxPlaceHolder, wx.Slider):
    def make(self, parent):
        wx.Slider.__init__(self, parent, **self.kwargs)
        return self


class ComboTreeBox(wxPlaceHolder, MSWComboTreeBox):
    def make(self, parent):
        MSWComboTreeBox.__init__(self, parent, **self.kwargs)
        return self

    #   def SetValue(self, val):
    #     super(ComboTreeBox, self).SetValue(val)
    #     self.element._text.SetInsertionPoint(0)

    #   def Getvalue(self, val):
    #     pass

    #   def GetClientData(self, selection):
    #     return self.element.GetClientData(selection)

    def SetOptions(self, choices):
        for category, options in choices:
            id = self.Append(category)  # @ReservedAssignment
            for option in options:
                self.Append(option, parent=id, clientData=category)
            if self.expand:
                self.GetTree().Expand(id)


class FloatSpin(wxPlaceHolder, FloatSpin_):
    def make(self, parent):
        FloatSpin_.__init__(self, parent, **self.kwargs)
        return self


class IpAddrCtrl(wxPlaceHolder, IpAddrCtrl_):
    def make(self, parent):
        IpAddrCtrl_.__init__(self, parent, **self.kwargs)
        return self


class CheckTreeCtrl(wxPlaceHolder, CustomTreeCtrl_):
    def make(self, parent):
        CustomTreeCtrl_.__init__(self, parent, **self.kwargs)
        return self

    def SetOptions(self, options):
        self.byname = {}
        root = self.AddRoot("")
        for parent, children in options:
            parentid = self.AppendItem(root, parent)
            self.byname[parent] = {}
            for child in children:
                childid = self.AppendItem(parentid, child, ct_type=1)
                self.byname[parent][child] = childid
        self.ExpandAll()

    def GetValue(self):
        value = {}
        root = self.GetRootItem()
        elem, cookie = self.GetFirstChild(root)
        while elem:
            parent = self.GetItemText(elem)
            value[parent] = {}
            sub, cookie2 = self.GetFirstChild(elem)
            while sub:
                child = self.GetItemText(sub)
                value[parent][child] = self.IsItemChecked(sub)
                sub, cookie2 = self.GetNextChild(elem, cookie2)
            elem, cookie = self.GetNextChild(root, cookie)
        return value

    def SetValue(self, val):
        for parent, children in self.byname.items():
            for child, item in children.items():
                try:
                    self.CheckItem(item, val[parent][child])
                except KeyError:
                    # Assume missing keys are for newly added entries.  Default to true.
                    self.CheckItem(item, True)


class HyperlinkCtrl(wxPlaceHolder, HyperLinkCtrl_):
    def make(self, parent):
        HyperLinkCtrl_.__init__(parent, -1, **self.kwargs)
        return self

    def GetValue(self):
        return self.GetURL()

    def SetValue(self, val):
        self.SetURL(val)

    def SetLabel(self, label):
        self.SetLabel(label)


class Console(wxPlaceHolder):
    def make(self, parent):
        self.element = Shell(parent=parent)
        return self.element


class DatePickerCtrl(wxPlaceHolder, DatePickerCtrl_):
    def make(self, parent):
        DatePickerCtrl_.__init__(self, parent, **self.kwargs)
        return self


class NumCtrl(wxPlaceHolder, NumCtrl_):
    def make(self, parent):
        NumCtrl_.__init__(self, parent, **self.kwargs)
        return self
