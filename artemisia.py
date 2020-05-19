# Drop pictures into a configured Raspberry Pi Zero W
# folder and this program will display them.

import wx

class DisplayPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)  # Any key presses are processed in the onKey handler
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update)
        self.timer.Start(1000)
        self.toggle = True

        self.displayWidth, self.displayHeight = wx.DisplaySize()  # What's the screen size in pixels

        self.blankScreen()

    def blankScreen(self):
        image = wx.Image(self.displayWidth, self.displayHeight)  # generates a black screen
        self.centerOnScreen(image)

    def centerOnScreen(self, image):
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(image))
        self.imageCtrl.Center()
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.imageCtrl)
        self.SetSizer(self.mainSizer)

    def fitToScreen(self, image):
        # scale the image, preserving the aspect ratio
        imageWidth = image.GetWidth()
        imageHeight = image.GetHeight()
        deltaWidth = self.displayWidth / imageWidth  # Ratio of Screen to Width
        deltaHeight = self.displayHeight / imageHeight  # Ratio of Screen to Height

        if deltaWidth < deltaHeight:         # If the width is smaller
            NewW = self.displayWidth         # set the width to the display
            NewH = imageHeight * deltaWidth  # adjust the height
        else:                                # If the height is smaller
            NewH = self.displayHeight        # set the height to the display
            NewW = imageWidth * deltaHeight  # adjust the width

        return image.Scale(NewW, NewH)

    def update(self, event):
        self.blankScreen()
        if self.toggle:
            image = wx.Image("./Images/SelfPortrait.jpg", wx.BITMAP_TYPE_ANY)
            self.toggle = False
        else:
            image = wx.Image("./Images/Paintings02.jpg", wx.BITMAP_TYPE_ANY)
            self.toggle = True

        image = self.fitToScreen(image)
        self.centerOnScreen(image)

    def onKey(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE: # If the escape key,
            self.timer.Stop()         # kill the timer,
            self.GetParent().Close()  # shutdown the app
        else:                         # otherwise
            event.Skip()              # Ignore the key press


class DisplayFrame(wx.Frame):
    """"""

    def __init__(self):
        wx.Frame.__init__(self, None, title="Image Viewer")
        panel = DisplayPanel(self)
        self.ShowFullScreen(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DisplayFrame()
    app.MainLoop()
