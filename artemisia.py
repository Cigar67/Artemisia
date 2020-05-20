# Drop pictures into a configured Raspberry Pi Zero W
# folder and this program will display them.

import wx
import os

IMAGES_FOLDER = "./Images/"
MESSAGES_FOLDER = "./Messages/"
MAX_DISPLAY_COUNT = 2 # Display a new image, in seconds
MAX_FOLDER_COUNT = 5  # Check for changes in image folder, in seconds

class DisplayPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.BLACK)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)     # All key presses are processed in the handler
        self.timer = wx.Timer(self)                # Create a timer,
        self.Bind(wx.EVT_TIMER, self.onTimerEvent) # bind it to the panel, call the handler when done
        self.timer.Start(1000)                     # and start it (in milliseconds)
        self.Bind(wx.EVT_PAINT, self.onPaint)      # Call handler when screen needs to be drawn

        self.images = []
        self.imageIndex = 0
        self.displayCount = 0
        self.folderCount = 0
        self.debugCount = 0 # Remove when debugging complete

        self.displayWidth, self.displayHeight = wx.DisplaySize()  # What's the screen size in pixels

        self.checkFolder()  # check if any changes to image folder

    def onKey(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE: # If the escape key,
            self.shutdown()           # close the app
        else:                         # otherwise,
            event.Skip()              # ignore the key press

    def onTimerEvent(self, event):                   # this event is called every second
        self.displayCount += 1                       # increment counters
        self.folderCount += 1                        #
        self.debugCount += 1 # Remove when debugging complete

        if (self.displayCount >= MAX_DISPLAY_COUNT): # check if MAX reached
            self.updateScreen()                      # time to show another picture
            self.Refresh()                           # generates an onPaint event
            self.displayCount = 0                    # reset the counter

        if (self.folderCount >= MAX_FOLDER_COUNT):   # check if MAX reached
            self.checkFolder()                       # check if any changes to image folder
            self.folderCount = 0                     # reset the counter

        if (self.debugCount >= 90): # Remove when debugging complete
            self.shutdown()         #

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        bitmap = self.images[self.imageIndex]['bitmap']
        point = self.images[self.imageIndex]['point']
        dc.DrawBitmap(bitmap, point.x, point.y)

    def shutdown(self):
        self.timer.Stop()         # kill the timer,
        self.GetParent().Close()  # shutdown the app

    def checkFolder(self):
        files = os.listdir(IMAGES_FOLDER) # Grab the names of all the files in the images folder
        if (len(files) == 0):             # If their aren't any files
            self.images.clear()           # empty the images list
            file = MESSAGES_FOLDER + "Empty Folder.png" #
            image = wx.Image(file, wx.BITMAP_TYPE_ANY)  # Remind the user
            self.addImage(file, image)                  #

        elif (len(files) != len(self.images)): # If the number of files in the folder doesn't match our list,
            self.images.clear()                # time to update our list
            for file in files:
                self.addImage(file, wx.Image(IMAGES_FOLDER + file, wx.BITMAP_TYPE_ANY))

    def addImage(self, file, image):
        image, point = self.fitToScreen(image)
        bitmap = wx.Bitmap(image)
        self.images.append({'name': file,  # Store the file name
                            'bitmap': bitmap,  # the image as a bitmap
                            'point': point})  # startX&Y for bitmap

    def fitToScreen(self, image):
        # scale the image, preserving the aspect ratio
        imageWidth = image.GetWidth()
        imageHeight = image.GetHeight()
        deltaWidth = self.displayWidth / imageWidth     # Ratio of Screen to Width
        deltaHeight = self.displayHeight / imageHeight  # Ratio of Screen to Height

        if deltaWidth < deltaHeight:             # If the width is smaller
            newWidth = self.displayWidth         # set the width to the display
            newHeight = imageHeight * deltaWidth # adjust the height
            newPoint = wx.Point(0, (self.displayHeight - newHeight) / 2)
        else:                                    # If the height is smaller
            newHeight = self.displayHeight       # set the height to the display
            newWidth = imageWidth * deltaHeight  # adjust the width
            newPoint = wx.Point((self.displayWidth - newWidth) / 2, 0)

        return (image.Scale(newWidth, newHeight), newPoint)

    def updateScreen(self):
        self.imageIndex += 1                      # Point to next image
        if (self.imageIndex >= len(self.images)): # Ensure wraparound
            self.imageIndex = 0                   # Point to first image


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
