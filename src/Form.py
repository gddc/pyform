  #!/usr/bin/env pythoninter
# -*- coding: utf-8 -*-

from collections import OrderedDict


import wx
from Controls import CheckBox, RadioButton, StaticText


class FormDialog(wx.Dialog):
  def __init__(self, parent, panel = None, title = "Unnamed Dialog",
               modal = False, sizes = (-1, -1), offset = None):
    wx.Dialog.__init__(self, parent, -1, title,
                       style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

    if panel is not None:
      self.panel = panel(self)
      self.SetTitle(self.panel.form.get('Title', title))
      self.panel.SetSizeHints(*sizes)

      ds = wx.GridBagSizer(self.panel.gap, self.panel.gap)
      ds.Add(self.panel, (0, 0), (1, 1), wx.EXPAND | wx.ALL, self.panel.gap)
      ds.Add(wx.StaticLine(self), (1, 0), (1, 1), wx.EXPAND | wx.RIGHT | wx.LEFT, self.panel.gap)

      self.bs = self.CreateButtonSizer(self.panel.form.get('Buttons', wx.OK | wx.CANCEL))
      ds.Add(self.bs, (2, 0), (1, 1), wx.ALIGN_RIGHT | wx.ALL, self.panel.gap)

      ds.AddGrowableCol(0)
      ds.AddGrowableRow(0)

      self.SetSizerAndFit(ds)
      self.Center()

      if offset:
        newpos = map(lambda x: x + offset, self.GetPositionTuple())
        self.SetPosition(wx.Point(*newpos))

      self.Bind(wx.EVT_BUTTON, self.panel.onOk, id = wx.ID_OK)
      self.Bind(wx.EVT_BUTTON, self.panel.onClose, id = wx.ID_CANCEL)

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
  def __init__(self, parent = None, id = -1, gap = 3, sizes = (-1, -1)): #@ReservedAssignment
    wx.Panel.__init__(self, parent, id)

    self.SetSizeHints(*sizes)
    self.gap = gap
    self.elements = OrderedDict([])

    if hasattr(self, 'form'):
      # Before building verify that several required sections exist in the form
      # definition object.
      if 'Defaults' not in self.form:
        self.form['Defaults'] = {}
      if 'Disabled' not in self.form:
        self.form['Disabled'] = []
      if 'Validators' not in self.form:
        self.form['Validators'] = {}
      if not self.form.has_key('Options'):
        self.form['Options'] = {}

      # Allow sub classes to add their own values or defaults.
      self.loadDefaults()
      self.loadOptions()
      self.build()
      self.bind()

  def HumanToMachine(self, name, value = ''):
    if 'Translations' in self.form:
      if name in self.form['Translations']:
        value = self.form['Translations'][name][1].get(value, value)
    return value

  def MachineToHuman(self, name, value = ''):
    if 'Translations' in self.form:
      if name in self.form['Translations']:
        value = self.form['Translations'][name][0].get(value, value)
    return value

  def Bind(self, evtType, evtFunc, evtSrc, call = False, *args, **kwargs):
    if isinstance(evtSrc, (str, unicode)):
      self.elements[evtSrc].ParentBind(self, evtType, evtFunc, *args, **kwargs)
    else:
      super(Form, self).Bind(evtType, evtFunc, evtSrc, *args, **kwargs)
    if call:
      evtFunc()

  def build(self):
    """
    The Build Method automates sizer creation and element placement by parsing
    a properly constructed object.
    """

    # The Main Sizer for the Panel.
    panelSizer = wx.BoxSizer(wx.VERTICAL)
    # Pass the outermost Parts and the container to the OrderedDict Parser.
    self.parseContainer(self.form['Parts'], panelSizer)
    self.SetSizerAndFit(panelSizer)

  def bind(self):
    pass

  def parseContainer(self, container, outerSizer, pos = None, span = None):
    for section in container.iteritems():
      region, proportion = self.parseSection(section)
      if isinstance(outerSizer, wx.GridBagSizer):
        outerSizer.Add(region, pos, span, border = self.gap,
                  flag = wx.ALIGN_CENTER_VERTICAL)
      else:
        outerSizer.Add(region, proportion, flag = wx.EXPAND | wx.ALL,
                       border = self.gap)


  def parseSection(self, section):
    container, blocks = section
    flags, _sep, display = container.rpartition('-')

    sizerProportion = 1 if 'G' in flags else 0
    if 'NC' in flags:
      sectionSizer = wx.BoxSizer(wx.VERTICAL)
      for block in blocks:
        self.parseBlock(block, sectionSizer)
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
    elif isinstance(block, tuple):
      item = self.makeRow(block)
    else:
      proportion = block.proportion
      item = self.makeElement(block)
    sectionSizer.Add(item, proportion, flag = wx.EXPAND | wx.ALL, border = self.gap)

  def makeElement(self, object): #@ReservedAssignment
    """
      In the form structure a dictionary signifies a single element.  A single
      element is automatically assumed to expand to fill available horizontal
      space in the form.
    """
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    flags = object.flags
    element = self.makeWidget(object)
    sizer.Add(element, 1, border = self.gap,
              flag = wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | flags)
    return sizer

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

#      sizer.Add(self.makeElement(field), proportion,
#                flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL)
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
        if isinstance(field, dict):
          flags = field.pop('flags', wx.ALL)
          rowGrowable = field.pop('rowGrowable', False)
          colGrowable = field.pop('colGrowable', False)
          span = field.pop('span', (1, 1))
          pos = field.pop('rowpos', row), field.pop('colpos', col)
        else:
          flags = field.flags
          rowGrowable = field.rowGrowable
          colGrowable = field.colGrowable
          span = field.span
          pos = field.rowpos or row, field.colpos or col

        if rowGrowable:
          sizer.AddGrowableRow(row)
        if colGrowable:
          sizer.AddGrowableCol(col)

        if isinstance(field, OrderedDict):
          self.parseContainer(field, sizer, pos, span)
        else:
          element = self.makeWidget(field)
          sizer.Add(element, pos, span, border = self.gap,
                    flag = wx.ALIGN_CENTER_VERTICAL | flags)
    return sizer

  def makeWidget(self, declarator):
    """
      This function actually creates the widgets that make up the form.
      Each element should provide a `make` method which takes as an argument
      it's parent, and returns a WX item (sizer, form element, etc).
      Other methods of not for each widget (defined with placeholders on
      the wxPlaceholder Class) are
        GetValue
        SetValue
        SetValidator
        SetOptions
    """

    element = declarator.make(self)
    if declarator.name:
      self.elements[declarator.name] = declarator
      # Options need to exist early.
      declarator.SetOptions(self.form['Options'].get(declarator.name, []))

      # We need to use the existing value if there isn't one in defaults
      # to prevent StaticText's from ending up blank.
      value = self.form['Defaults'].get(declarator.name, declarator.GetValue())

      # Assign or populate any fields requiring it.
      declarator.SetValue(self.MachineToHuman(declarator.name, value))
      declarator.SetValidator(self.form['Validators'].get(declarator.name, None))
    return element

  def loadDefaults(self):
    pass

  def loadOptions(self):
    pass

  def onOk(self, evt):
    self.onClose(evt)

  def onClose(self, evt):
    self.GetParent().FocusNext()

  def fieldValidate(self):
    if not self.form.has_key('Validators'):
      return True
    Success, Messages = True, []
    for name, field in self.elements.items():
      if name in self.form['Validators']:
        s, m = field.Validate()
        if not s:
          Success = False
          Messages.extend(m)
    if Messages:
      text = '\r\n'.join(Messages)
      wx.MessageDialog(self, text, "Form Field Error", wx.OK).ShowModal()

    return Success

if __name__ == "__main__":
  from Demos import DemoForm, DemoFormGrowable, DemoNested, DemoNestedHorizontal, \
      ComplicatedDemo

  app = wx.PySimpleApp()
  f = wx.Frame(None)
  f.Show()
  FormDialog(parent = f, panel = DemoForm)
  FormDialog(parent = f, panel = DemoFormGrowable)
  FormDialog(parent = f, panel = DemoNested)
  FormDialog(parent = f, panel = DemoNestedHorizontal)
  FormDialog(parent = f, panel = ComplicatedDemo)

  app.MainLoop()
