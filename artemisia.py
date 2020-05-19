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
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)  # Any key presses are processed in the onKey handler
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimerEvent)
        self.timer.Start(1000)
        # self.toggle = True
        self.images = []
        self.imageIndex = 0
        self.displayCount = 0
        self.folderCount = 0

        self.displayWidth, self.displayHeight = wx.DisplaySize()  # What's the screen size in pixels

        self.blankScreen()
        self.checkFolder()  # check if any changes to image folder

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

    def onTimerEvent(self, event):                   # this event is called every second
        self.displayCount += 1                       # increment counters
        self.folderCount += 1                        #

        if (self.displayCount >= MAX_DISPLAY_COUNT): # check if MAX reached
            self.updateScreen()                      # time to show another picture
            self.displayCount = 0                    # reset the counter

        if (self.folderCount >= MAX_FOLDER_COUNT):   # check if MAX reached
            self.checkFolder()                       # check if any changes to image folder
            self.folderCount = 0                     # reset the counter

    def checkFolder(self):
        files = os.listdir(IMAGES_FOLDER) # Grab the names of all the files in the images folder
        if (len(files) == 0):             # If their aren't any files
            image = wx.Image(MESSAGES_FOLDER + "Empty Folder.png", wx.BITMAP_TYPE_ANY) # Remind the user
            image = self.fitToScreen(image)
            self.centerOnScreen(image)
        elif (len(files) != len(self.images)): # If our file list doesn't match the folder list
            self.images.clear()                # Time to update our file list
            for file in files:
                data = os.stat(IMAGES_FOLDER + file)
                image = wx.Image(IMAGES_FOLDER + file, wx.BITMAP_TYPE_ANY)
                self.images.append({'fName':file,             # Store the file name
                                    'image':image,            # the image
                                    'modTime':data.st_mtime}) # and last modified time

    def updateScreen(self):
        self.blankScreen()

        image = self.images[self.imageIndex]['image']
        image = self.fitToScreen(image)
        self.centerOnScreen(image)

        self.imageIndex += 1
        if (self.imageIndex >= len(self.images)): # Ensure wraparound
            self.imageIndex = 0

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
