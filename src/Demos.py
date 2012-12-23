'''
Created on Dec 16, 2012

@author: daniel
'''

from Form import Form
from collections import OrderedDict
from Controls import *


class DemoForm(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': "Demo Form 1",
      'Parts':  OrderedDict([
        ('Test Section', [
          StaticText(label = "This is the first attempt at a demo.")
        ])
      ])
    }
    Form.__init__(self, parent, **kwargs)

class DemoFormGrowable(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': "Demo with Growable Regions",
      'Parts':  OrderedDict([
        ('G-Test Growable Form', [
          StaticText(label = "This Box Sizer will use up available space.")
        ])
      ])
    }
    Form.__init__(self, parent, **kwargs)

class DemoNested(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': "Nexted Containers",
      'Parts':  OrderedDict([
        ('G-Test Nested Growables', [
          OrderedDict([
            ('G-Inner Growable', [
              StaticText(label = 'This Test is a bit less likely to work.')
            ])
          ]),
          OrderedDict([
            ('G-Inner Growable 2', [
              StaticText(label = 'This Test is a bit less likely to work.')
            ])
          ])
        ])
      ])
    }
    Form.__init__(self, parent, **kwargs)

class DemoNestedHorizontal(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': 'Horizontally Nested',
      'Parts':  OrderedDict([
        ('G-Test Nested Growables', [
          (OrderedDict([
             ('G-Inner Growable', [
               StaticText(label = 'This Test is a bit less likely to work.')
             ])
           ]),
           OrderedDict([
             ('G-Inner Growable 2', [
               StaticText(label = 'This Test is a bit less likely to work.')
             ])
           ]))
        ])
      ])
    }
    Form.__init__(self, parent, **kwargs)


class ComplicatedDemo(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': 'Getting More Complicated',
      'Parts':  OrderedDict([
        ('G-Test Nested Growables', [
          (OrderedDict([
             ('G-Inner Growable', [
               StaticText(label = 'This Test is a bit less likely to work.')
             ])
           ]),
           OrderedDict([
             ('G-Inner Growable 2', [
               StaticText(label = 'This Test is a bit less likely to work.')
             ])
           ])),
          [(StaticText(label = "Inner 1"),
            StaticText(label = "Inner 2"),
            OrderedDict([
              ('G-Inner Growable 2', [
                StaticText(label = 'This Test is a bit less likely to work.'),
                (CheckBox(name = 'Check1', label = "A few samples."),
                 StaticText(label = "Like This."))
              ])
            ]),
            StaticText(label = "Another Inner"))]
        ])
      ])
    }
    Form.__init__(self, parent, **kwargs)


class ComprehensiveDemo(Form):
  def __init__(self, parent, **kwargs):
    self.form = {
      'Title': 'Comprehensively Complicated',
      'Parts':  OrderedDict([
        ('Lots Of Types of Elements', [
          # These first several are stand alone.                               
          FontPicker(name = 'FontPicker'),
          StaticText(label = "We've seen these.  This one is unnamed."),
          CheckBox(name = 'Check1', label = "Checkboxes are fun.  This one "
                                            "controls the input below it."),
          TextCtrl(name = 'Input1'),
          # Then several in a row
          (StaticText(label = "Passwords can be accomodated."),
           PassCtrl(name = "Pass1")),
          Button(name = 'Button1', label = "This is just a button."),
          TreeCtrl(name = 'Tree1'), #todo tree needs populated.
          # Grids take place here.
          [(ComboBox(name = 'Combo1', choices = ['1', '2', '3']),
            FloatSpin(name = 'FloatSpin1', min_val = 0, max_val = 30, digits = 2,
                      increment = 0.1, size = (30, -1), flags = wx.EXPAND | wx.ALL),
            StaticText(label = "Ip Addresses are fairly common."),
            IpAddrCtrl(name = "IpAddresses")),
           (RadioButton(name = "R1", label = "Radios"),
            RadioButton(name = "R2", label = "can be linked"),
            RadioButton(name = "R3", label = "Or", style = wx.RB_GROUP),
            RadioButton(name = "R4", label = "Disconnected"))]
        ]),
        ('G-Another Container - With Nesting (Take Care).', [
          # Are you paying close attention here?  We're nesting OrderedDict's
          # in tuple's to get side-by-side BoxSizers
          (OrderedDict([
             ('Inner Container 1', [
               (StaticText(label = "Colors Are Good."),
                ColorPicker(name = "Color1"))
             ])
           ]),
           OrderedDict([
             ('Inner Contaner 2', [
               Slider(name = "Slider1")
             ])
           ]),
           OrderedDict([
             ('Inner Contaner 3', [
               Slider(name = "Slider2", minValue = 1, maxValue = 100,
                      style = wx.SL_LABELS)
             ])
           ])),
          # Which we're going to place above another container.
          OrderedDict([
            ('G-This is getting kind of deeply nested.', [
              OrderedDict([
                ("G-But we're showing just how intricate", [
                  StaticText(label = "your forms can be.")
                ])
              ])
            ])
          ])
        ])
      ])
    }
    super(ComprehensiveDemo, self).__init__(parent, **kwargs)

  def bind(self):
    self.Bind(wx.EVT_CHECKBOX, self.onCheck1, 'Check1', True)
    super(ComprehensiveDemo, self).bind()

  def onCheck1(self, evt = None):
    self.elements['Input1'].Enable(self.elements['Check1'].GetValue())


class AlternateDeclaration(Form):
  """
    This example provdies a different way to declare forms, in case the
    nesting from the previous example was a bit overwhelming.
  """
  def __init__(self, parent, **kwargs):
    self.form = {}
    self.form['Title'] = "Easier to Read (?)"
    defaults = self.form['Defaults'] = {}
    options = self.form['Options'] = {}
    parts = self.form['Parts'] = OrderedDict([])
    parts['Outermost'] = outer = list()
    outer.append(CheckBox(name = 'Check1', label = "Just a checkbox."))
    outer.append(StaticText(label = "And some text."))
    outer.append((StaticText(label = "These should form"),
                  StaticText(label = "a row.")))
    inner = OrderedDict([])
    inner['Sub 1'] = sub1 = list()
    sub1.append(ComboBox(name = 'Combo'))
    defaults['Combo'] = 'Default Value'
    options['Combo'] = map(str, range(10))
    outer.append(inner)
    super(AlternateDeclaration, self).__init__(parent, **kwargs)


class GridDemos(Form):
  def __init__(self, parent, **kwargs):
    self.form = {}
    self.form['Title'] = "Nested Grids"
    parts = self.form['Parts'] = OrderedDict([])
    for row in range(10):
      row_list = parts['Row %d' % row] = list()
      cols = list()
      for col in range(10):
        inner = OrderedDict()
        innermost = inner['Col %d' % col] = list()
        innermost.append(StaticText(label = "%d x %d" % (row, col)))
        cols.append(inner)
      row_list.append(tuple(cols))
    super(GridDemos, self).__init__(parent, **kwargs)


class DemoLeftStacked(Form):
  def __init__(self, parent, **kwargs):
    self.form = {'Title': 'Left Stacked Demo'}
    parts = self.form['Parts'] = OrderedDict()
    outermost = parts['G-Outermost'] = list()
    left, right = OrderedDict(), OrderedDict()
    outermost.append(Row((left, right), rowGrowable = True, proportion = 1))
    l1 = left['G-Left Top'] = list()
    l1.append(StaticText(label = 'Left Top Inner'))
    l2 = left['G-Left Bottom'] = list()
    l2.append(StaticText(label = 'Left Bottom Inner'))
    r1 = right['G-Right'] = list()
    r1.append(TextCtrl(name = 'Text', style = wx.TE_MULTILINE,
                       colGrowable = True, rowGrowable = True, proportion = 1))


    super(DemoLeftStacked, self).__init__(parent, **kwargs)

