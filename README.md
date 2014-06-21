pyform - an expressive wxPython wrapper library
======

pyform is my attempt at simplifying the work that goes into
creating User Interfaces in wxPython.  If you have ever used
code like this you know what I am referring to:

    sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
    sizer_2 = wx.BoxSizer(wx.VERTICAL)
    sizer_1.Add(myControl)
    sizer_2.Add(sizer1)
    # And so on forever, it feels like.
  
While that's not the end of the world for simple UI's, it
gets out of hand quickly for complicated layouts, nested
containers or elements, etc.  It becomes excessively
redundant when dealing with lots of Controls and makes
rearranging the interface after creating it downright painful.

Enter pyform to the rescue.  Pyform parses a structured
declaration into meaningful sizers auto-magically.  It 
combines arguments from Controls and Containers (I'm looking
you, proportion) into the declaration for the Controls
themselves.  Declare an element with the properties it needs,
let pyform sort out if those properties only matter when
adding it to a Sizer.

For examples of how to put it to use, check out the Demos.
