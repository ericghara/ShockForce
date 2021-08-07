from src import ShockForce, SecondaryWindows
from matplotlib import animation
from copy import copy
from PyQt5 import QtCore

class Wrapper:

    def __init__(self):
        self.FPS = 60
        self.simType = "a"
        self.simTypeCBoxDict = {
            "Spring Rate": "s",
            "Spring Preload": "p",
            "Airgap": "a"
        }
        self.simTypeUnitsDict = {
            "s": ("kg/mm", "kg/mm", "sec"),
            "p": ("cm", "cm", "sec"),
            "a": ("cm", "cm", "sec")
        } # B unit, E unit, Duration unit
        self.simTypeDefaultValsDict = {
            "s": (0.00, 1.30, 8, 1),
            "p": (0.00, 10.5, 8, 1),
            "a": (0.05, 10.5, 8, 1)
        }  # Format: simType : (B, E, Animation Length (s), Annotations 0/1
        self.simTypeValMinMax = {
            "s": {"B" : (0.00, 9.99), "E" : (0.00, 9.99), "D" : (0,30)},
            "p": {"B" : (0.00, 10.5), "E" : (0.00, 10.5), "D" : (0, 30)},
            "a": {"B" : (0.01, 10.5), "E" : (0.01, 10.5), "D" : (0, 30)}
        } # format: simtype: {input : (min,max)...}
        self.anim = None

    def comboBoxLogic(self, app, index):
        dictKey = [*self.simTypeCBoxDict.keys()][index]
        simType = self.simTypeCBoxDict[dictKey]
        self.simType = simType
        app.refreshLabels()
        app.refreshInputs(simType)

    def SimulateWrapper(self, B, E, duration, annotations, simType=None):
        if simType == None:
            simType = self.simType
        elif simType in self.simTypeCBoxDict.keys():
            #Manually set simType, haven't tested this feature
            self.simType = simType
        else:
            print("Error - SimulateWrapper received unrecognized simType: %s" % str(simType))
        step = self.durationLogic(B, E, duration)
        sim = ShockForce.Simulate()
        fig, ims = sim.get_data(simType, B, E, step, annotations)
        ims += ims[-2:0:-1]  # Reversed ims minus first and last frame (to allow reflection like loop)
        return fig, ims

    def durationLogic(self, B, E, duration):
        #Returns step size to fit duration based on FPS
        frames = duration*self.FPS/2  # Note Divide by 2 because we're reflecting video by appending list of inverted ims to end of generated images
        step = (E-B)/frames
        return step

    def saveLogic(self,app, fig, ims):
        returnVal = True
        Save = SecondaryWindows.SaveDialog()
        path, filetype = Save.dialog()
        if (path, filetype) == (False, False): # user pressed cancel
            return False
        elif "." != path[-4]: #fixes bug in linux env where no ext is added to filename
            path = path + filetype[-5:-1]
        elif filetype[-5:-1] not in path: # Fixes a bug where user selects an existing file of different extension QFileDialog butchers path
            path = path[:-4] + filetype[-5:-1]
        app.canvas.setVisible(False)
        app.loadingMessage("s")
        print("Saving %s to %s" % (filetype[-4:-1], path))
        newfig = copy(fig)  # Need to copy or we will change the animation currently being displayed in mainwindow
        if "htm" in filetype:
            length = int(len(ims) / 2 + 1)  # Calculates original length before reflection
            frames = ims[:length]  # Slices ims to original length
            anim = animation.ArtistAnimation(newfig, frames, interval=10, blit=True)
            jsAnim = anim.to_jshtml(default_mode="reflect")
            try:
                with open(path, "w") as f:
                    f.write(jsAnim)
            except:
                print("Error saving file at: %s" % fullPath)
                print("check save path and ensure you have permission to access destination folder.")
                returnVal = False
        elif "gif" in filetype:
            self.anim.save(path, writer='imagemagick', fps=self.FPS) #Note we are calling self.anim which is the anim being displayed in mainwindow

        elif "mp4" in filetype:
            self.anim.save(path, writer='ffmpeg', fps=self.FPS)  # Note we are calling self.anim which is the anim being displayed in mainwindow"""
        app.delLoadingMessage()
        app.canvas.setVisible(True)
        return returnVal
