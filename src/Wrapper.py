from src import ShockForce

class Wrapper():
    def __init__(self):
        self.FPS = 60
        self.simType = "s"
        self.simTypeCBoxDict = {
            "Spring Rate": "s",
            "Spring Preload": "p",
            "Airgap": "a"
        }
        self.simTypeUnitsDict = {
            "s": "kg/mm",
            "p": "cm",
            "a": "cm"
        }
        self.simTypeDefaultValsDict = {
            "s": (0.00, 1.30, 4),
            "p": (0.00, 10.5, 4),
            "a": (0.05, 10.5, 4)
        }  # Format: simType : (B, E, Animation Length (s)
        self.simTypeValMinMax = {
            "s": {"BE" : (0.00, 9.99), "D" : (0,20)},
            "p": {"BE" : (0.00, 10.5), "D" : (0, 20)},
            "a": {"BE" : (0.01, 10.5), "D" : (0, 20)}
        }

    def x(self):
        return self.SimTypeCBoxDict

    def comboBoxLogic(self, app, index):
        dictKey = [*self.simTypeCBoxDict.keys()][index]
        simType = self.simTypeCBoxDict[dictKey]
        #Remove this conditional check once changing sweep feature implemented
        if simType in self.simTypeCBoxDict.values():
            B, E, D = self.simTypeDefaultValsDict[simType]
            fig, ims = self.SimulateWrapper(simType, B, E, D)
        else:
            print('Error comboBoxLogic received unrecognized SimType: "%s' % simType)
            return -1
        app.refreshAnimation(fig, ims)

    def SimulateWrapper(self, simType, B, E, duration):
        step = self.durationLogic(B, E, duration)
        sim = ShockForce.Simulate()
        fig, ims = sim.get_data(simType, B, E, step)
        ims += ims[-2:0:-1]  # Reversed ims minus first and last frame (to allow reflection like loop)
        return fig, ims

    def durationLogic(self, B, E, duration):
        #Returns step size to fit duration based on FPS
        frames = duration*self.FPS
        step = (E-B)/frames
        return step

    def goButtonLogic(self):
        #get combobox value
        #get B
        #get E
        #get duration
        #Check for input errors
        # B < E
        # BED policy from dicts
        #get annotation True/False
        pass