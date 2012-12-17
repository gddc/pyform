'''
Created on Dec 16, 2012

@author: daniel
'''

from Form import Form
from collections import OrderedDict
from Controls import StaticText, CheckBox


class DemoForm(Form):
  def __init__(self, parent):
    self.form = {
      'Parts':  OrderedDict([
        ('Test Section', [
          StaticText(label = "This is the first attempt at a demo.")
        ])
      ])
    }
    Form.__init__(self, parent)

class DemoFormGrowable(Form):
  def __init__(self, parent):
    self.form = {
      'Parts':  OrderedDict([
        ('G-Test Growable Form', [
          StaticText(label = "This Box Sizer will use up available space.")
        ])
      ])
    }
    Form.__init__(self, parent)

class DemoNested(Form):
  def __init__(self, parent):
    self.form = {
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
    Form.__init__(self, parent)

class DemoNestedHorizontal(Form):
  def __init__(self, parent):
    self.form = {
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
    Form.__init__(self, parent)


class ComplicatedDemo(Form):
  def __init__(self, parent):
    self.form = {
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
    Form.__init__(self, parent)


