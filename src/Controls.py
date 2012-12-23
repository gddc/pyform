'''
Created on Nov 9, 2011

@author: daniel

This module contains custom classes to provide functionality from
the wx module in specific ways.
'''

from wx.py.crust import Shell
from wx.lib.combotreebox import ComboTreeBox as _ComboTreeBox
from wx.lib.agw.floatspin import FloatSpin as _FloatSpin
from wx.lib.masked.ipaddrctrl import IpAddrCtrl as _IpAddrCtrl
from infinity77libs.CustomTreeCtrl import CustomTreeCtrl as _CustomTreeCtrl
from win32wnet import WNetGetUniversalName
import wx
from util.FlowSizer import FlowSizer

class _CustomFontCtrl(wx.Button):
  """
    This custom font control class provides a Font Dialog that displays with
    EnableEffects set to False.  This is used in place of the built-in
    FontPickerCtrl which does not allow for the disabling of features
    that are currently not supported.
  """
  def __init__(self, *args, **kwargs):
    super(_CustomFontCtrl, self).__init__(*args, **kwargs)
    self.font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
    self.Bind(wx.EVT_BUTTON, self.onClick)

  def onEnumFonts(self, data):
    self.installed = data['font-names']

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
    self.SetLabel(', '.join(map(unicode, (self.font.GetFaceName(), self.font.GetPointSize()))))
    self.SetFont(self.font)

  def GetSelectedFont(self):
    return self.font

  def SetFontFromDesc(self, desc):
    self.font.SetNativeFontInfoFromString(desc)
    self.SetLabel(', '.join(map(unicode, (self.font.GetFaceName(), self.font.GetPointSize()))))
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
    self.name = kwargs.pop('name', None)
    self.proportion = kwargs.pop('proportion', 0)
    self.flags = kwargs.pop('flags', wx.ALL)
    self.rowGrowable = kwargs.pop('rowGrowable', False)
    self.colGrowable = kwargs.pop('colGrowable', False)
    self.span = kwargs.pop('span', (1, 1))
    self.size = kwargs.get('size', (-1, -1))
    self.rowpos = kwargs.pop('rowpos', None)
    self.colpos = kwargs.pop('colpos', None)
    self.expand = kwargs.pop('expand', True)
    self.kwargs = kwargs

  def __iter__(self):
    return iter(self.items)

class wxPlaceHolder(object):
  def __init__(self, **kwargs):
    # Pull anything that doesn't belong to the actual element out of the 
    # kwargs for use when adding to the sizer, etc.
    self.name = kwargs.get('name', None)
    self.proportion = kwargs.pop('proportion', 0)
    self.flags = kwargs.pop('flags', wx.ALL)
    self.rowGrowable = kwargs.pop('rowGrowable', False)
    self.colGrowable = kwargs.pop('colGrowable', False)
    self.span = kwargs.pop('span', (1, 1))
    self.size = kwargs.get('size', (-1, -1))
    self.rowpos = kwargs.pop('rowpos', None)
    self.colpos = kwargs.pop('colpos', None)
    self.expand = kwargs.pop('expand', True)
    self.local = kwargs.pop('local', False)
    self.admin = kwargs.pop('admin', False)
    self.maxlength = kwargs.pop('maxlength', None)
    self.kwargs = kwargs

  def GetId(self):
    return self.element.GetId()

  def Enable(self, state):
    self.element.Enable(state)

  def GetInsertionPoint(self):
    return self.element.GetInsertionPoint()

  def SetInsertionPoint(self, idx):
    return self.element.SetInsertionPoint(idx)

  def GetSelection(self):
    return self.element.GetSelection()

  def SetOptions(self, options):
    pass

  def SetFocus(self):
    return self.element.SetFocus()

  def SetValue(self, val):
    return self.element.SetValue(val)

  def GetValue(self):
    return self.element.GetValue()

  def ParentBind(self, parent, evtType, evtFunc, *args, **kwargs):
    return wx.Panel.Bind(parent, evtType, evtFunc, self.element, *args, **kwargs)

  def Validate(self):
    if hasattr(self, 'validator'):
      return self.validator().Validate(self.element)
    return True, []

  def SetValidator(self, validator):
    self.validator = validator


class Panel(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.Panel(parent, **self.kwargs)
    return self.element


class FontPicker(wxPlaceHolder):
  def make(self, parent):
    self.element = _CustomFontCtrl(parent, **self.kwargs)
    return self.element

  def GetValue(self):
    return self.element.GetSelectedFont().GetNativeFontInfoDesc()

  def SetValue(self, val):
    self.element.SetFontFromDesc(val)

  def GetSelectedFont(self):
    return self.element.GetSelectedFont()


class StaticText(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    bold = self.kwargs.pop('bold', False)
    size = self.kwargs.pop('fontsize', None)
    self.element = wx.StaticText(parent, **self.kwargs)
    font = self.element.GetFont()
    if size is not None:
      font.SetPointSize(size)
    if bold:
      font.SetWeight(wx.BOLD)
    self.element.SetFont(font)

    return self.element

  def SetValue(self, val):
    self.element.SetLabel(val)

  def GetValue(self):
    return self.element.GetLabel()

class TextFlow(wxPlaceHolder):
  def make(self, parent):
    bold = self.kwargs.pop('bold', False)
    size = self.kwargs.pop('fontsize', None)
    self.element = FlowSizer()
    self.words = []
    for word in self.kwargs['label'].split():
      text = wx.StaticText(parent, label = word)
      if size or bold:
        font = text.GetFont()
        if size is not None:
          font.SetPointSize(size)
        if bold:
          font.SetWeight(wx.BOLD)
        text.SetFont(font)
      self.words.append(text)
      self.element.Add(text, flag = wx.TOP | wx.RIGHT, border = 2)
    return self.element

  def SetValue(self, val):
    pass

  def GetValue(self):
    return ' '.join(word.GetLabel() for word in self.words)


class CheckBox(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    self.element = wx.CheckBox(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    self.element.SetValue(bool(val))


class TextCtrl(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    self.element = wx.TextCtrl(parent, **self.kwargs)
    if self.maxlength:
      self.element.SetMaxLength(self.maxlength)
    return self.element

  def Remove(self, *args):
    return self.element.Remove(*args)

  def WriteText(self, text):
    return self.element.WriteText(text)

class PassCtrl(TextCtrl):
  def make(self, parent):
    self.kwargs['style'] = wx.TE_PASSWORD
    return super(PassCtrl, self).make(parent)

  def SetValue(self, val):
    self.element.SetValue(val)

  def GetValue(self):
    return self.element.GetValue()

  def GetRawValue(self):
    return self.element.GetValue()


class Button(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    self.element = wx.Button(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    pass

  def GetValue(self):
    pass

class ListHolder(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    self.element = self.kwargs['list'](parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    pass

  def GetValue(self):
    return self.element.GetValue()

class FolderBrowser(wxPlaceHolder):
  def make(self, parent): #@ReservedAssignment
    self.parent = parent
    self.element = wx.DirPickerCtrl(parent, **self.kwargs)
    self.element.GetTextCtrl().SetEditable(False)
    return self.element

  def SetFocus(self):
    super(FolderBrowser, self).SetFocus()

  def Enable(self, state):
    self.element.Enable(state)

  def ParentBind(self, parent, evtType, evtFunc, *args, **kwargs):
    wx.Panel.Bind(parent, wx.EVT_DIRPICKER_CHANGED, evtFunc, self.element)

  def SetValue(self, val):
    self.element.SetPath(val)

  def GetValue(self):
    val = self.element.GetPath()
    try:
      val = WNetGetUniversalName(val)
    except:
      pass
    return val

  def Validate(self):
    return self.validator().Validate(self.element)



class TreeCtrl(wxPlaceHolder):
  def make(self, parent):
    self.parent = parent
    self.element = wx.TreeCtrl(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    pass

  def GetValue(self, selection = None):
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
        return '\\'.join(pieces[1:])
      else:
        return None
    return self.element.GetItemText(selection)

  def GetSelection(self):
    return self.element.GetSelection()

  def SetImageList(self, il):
    return self.element.SetImageList(il)

  def AddRoot(self, *args):
    return self.element.AddRoot(*args)

  def AppendItem(self, *args, **kwargs):
    return self.element.AppendItem(*args, **kwargs)

  def GetPyData(self, item):
    return self.element.GetPyData(item)

  def SetPyData(self, item):
    return self.element.SetPyData(item)

  def SetItemHasChildren(self, *args):
    return self.element.SetItemHasChildren(*args)

  def GetItemParent(self, item):
    return self.element.GetItemParent(item)

  def GetItemText(self, item):
    return self.element.GetItemText(item)

  def Expand(self, leaf):
    return self.element.Expand(leaf)

  def GetChildrenCount(self, item):
    return self.element.GetChildrenCount(item, False)



class ComboBox(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.ComboBox(parent, **self.kwargs)
    return self.element

  def SetOptions(self, options):
    self.element.Clear()
    self.element.AppendItems(options)

  def SetValue(self, val):
    self.element.SetValue(unicode(val))

  def Clear(self):
    self.element.Clear()

  def Append(self, option):
    self.element.Append(option)


class SpinCtrl(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.SpinCtrl(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    self.element.SetValue(int(val))


class RadioButton(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.RadioButton(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    self.element.SetValue(bool(val))


class StaticBitmap(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.StaticBitmap(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    pass


class ColorPicker(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.ColourPickerCtrl(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    self.element.SetColour(wx.Colour(**eval(val)))

  def GetValue(self):
    color = self.element.GetColour()
    return unicode({'red': color.Red(),
                    'green': color.Green(),
                    'blue': color.Blue()})


class Slider(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.Slider(parent, **self.kwargs)
    return self.element


class ComboTreeBox(wxPlaceHolder):
  def make(self, parent):
    self.element = _ComboTreeBox(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    super(ComboTreeBox, self).SetValue(val)
    self.element._text.SetInsertionPoint(0)

  def Getvalue(self, val):
    pass

  def GetClientData(self, selection):
    return self.element.GetClientData(selection)

  def SetOptions(self, choices):
    for category, options in choices:
      id = self.element.Append(category) #@ReservedAssignment

      for option in options:
        self.element.Append(option, parent = id, clientData = category)

      if self.expand:
        self.element.GetTree().Expand(id)


class FloatSpin(wxPlaceHolder):
  def make(self, parent):
    self.element = _FloatSpin(parent, **self.kwargs)
    return self.element

  def SetValue(self, val):
    self.element.SetValue(float(val))


class IpAddrCtrl(wxPlaceHolder):
  def make(self, parent):
    self.element = _IpAddrCtrl(parent, **self.kwargs)
    return self.element


class CheckTreeCtrl(wxPlaceHolder):
  def make(self, parent):
    self.element = _CustomTreeCtrl(parent, **self.kwargs)
    return self.element

  def SetOptions(self, options):
    self.byname = {}
    root = self.element.AddRoot('')
    for parent, children in options:
      parentid = self.element.AppendItem(root, parent)
      self.byname[parent] = {}
      for child in children:
        childid = self.element.AppendItem(parentid, child, ct_type = 1)
        self.byname[parent][child] = childid
    self.element.ExpandAll()

  def GetValue(self):
    value = {}
    root = self.element.GetRootItem()
    elem, cookie = self.element.GetFirstChild(root)
    while elem:
      parent = self.element.GetItemText(elem)
      value[parent] = {}
      sub, cookie2 = self.element.GetFirstChild(elem)
      while sub:
        child = self.element.GetItemText(sub)
        value[parent][child] = self.element.IsItemChecked(sub)
        sub, cookie2 = self.element.GetNextChild(elem, cookie2)
      elem, cookie = self.element.GetNextChild(root, cookie)
    return value

  def SetValue(self, val):
    for parent, children in self.byname.items():
      for child, item in children.items():
        try:
          self.element.CheckItem(item, val[parent][child])
        except KeyError:
          # Assume missing keys are for newly added entries.  Default to true.
          self.element.CheckItem(item, True)


class HyperlinkCtrl(wxPlaceHolder):
  def make(self, parent):
    self.element = wx.HyperlinkCtrl(parent, -1, **self.kwargs)
    return self.element

  def GetValue(self):
    return self.element.GetURL()

  def SetValue(self, val):
    self.element.SetURL(val)

  def SetLabel(self, label):
    self.element.SetLabel(label)

class Console(wxPlaceHolder):
  def make(self, parent):
    self.element = Shell(parent = parent)
    return self.element
