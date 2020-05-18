# Drop pictures into a configured Raspberry Pi Zero W
# folder and this program will display them.

import wx

class DisplayPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)  # Any key presses are processed in the onKey handler

        self.displayWidth, self.displayHeight = wx.DisplaySize()  # What's the screen size in pixels

        img = wx.Image(self.displayWidth, self.displayHeight)  # generates a black screen
        # img = wx.Image("./Images/SelfPortrait.jpg", wx.BITMAP_TYPE_ANY)
        # img = wx.Image("./Images/Paintings02.jpg", wx.BITMAP_TYPE_ANY)
        # img = self.expandImageToScreen(img)

        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainSizer.Add(self.imageCtrl, 0, wx.CENTER | wx.CENTER)
        self.SetSizer(self.mainSizer)

    def expandImageToScreen(self, image):
        # scale the image, preserving the aspect ratio
        imageWidth = image.GetWidth()
        imageHeight = image.GetHeight()
        deltaWidth = self.displayWidth / imageWidth  # Ratio of Screen to Width
        deltaHeight = self.displayHeight / imageHeight  # Ratio of Screen to Height

        if deltaWidth < deltaHeight:  # If the width is smaller
            NewW = self.displayWidth  # set the width to the display
            NewH = imageHeight * deltaWidth  # adjust the height
        else:  # If the height is smaller
            NewH = self.displayHeight  # set the height to the display
            NewW = imageWidth * deltaHeight  # adjust the width

        return image.Scale(NewW, NewH)

    def onKey(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE: # If the escape key,
            self.GetParent().Close()  # shutdown the app
        else:                         # otherwise
            event.Skip()              # Ignore the key press


class DisplayFrame(wx.Frame):
    """"""

    def __init__(self):
        wx.Frame.__init__(self, None, title="Test FullScreen")
        panel = DisplayPanel(self)
        self.ShowFullScreen(True)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DisplayFrame()
    app.MainLoop()
