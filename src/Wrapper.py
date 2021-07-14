from src import ShockForce

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
            "s": (0.00, 1.30, 4),
            "p": (0.00, 10.5, 4),
            "a": (0.05, 10.5, 4)
        }  # Format: simType : (B, E, Animation Length (s)
        self.simTypeValMinMax = {
            "s": {"B" : (0.00, 9.99), "E" : (0.00, 9.99), "D" : (0,20)},
            "p": {"B" : (0.00, 10.5), "E" : (0.00, 10.5), "D" : (0, 20)},
            "a": {"B" : (0.01, 10.5), "E" : (0.01, 10.5), "D" : (0, 20)}
        } # format: simtype: {input : (min,max)...}

    def comboBoxLogic(self, app, index):
        dictKey = [*self.simTypeCBoxDict.keys()][index]
        simType = self.simTypeCBoxDict[dictKey]
        self.simType = simType
        app.refreshLabels()
        app.refreshLEdits(simType)

    def SimulateWrapper(self, B, E, duration, simType=None):
        if simType == None:
            simType = self.simType
        elif simType in self.simTypeCBoxDict.keys():
            #Manually set simType, haven't tested this feature
            self.simType = simType
        else:
            print("Error - SimulateWrapper received unrecognized simType: %s" % str(simType))
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

