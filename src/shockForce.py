import pandas as pd
from math import pi, tan, degrees
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from IPython.display import HTML
import string
from os.path import join

class ShockForce:
    # Collection of methods to model static forces from shock compression 
    def __init__(self, diameter=4.1, airgap=10.5, springRate=.87, preload=0):
        self.atmPres = 1.033 # kg/cm2 absolute
        self.P1 = self.atmPres # kg/cm2 absolute
        self.P2 = None # kg/cm2 absolute
        self.area = (diameter/2)**2*pi # cm2
        self.airgap = airgap # cm
        self.V1 = airgap*self.area # cm**3
        self.V2 = None # cm**3
        self.stroke = 0
        self.springRate = springRate # kg/mm
        self.preload = preload # cm
        self.gasForce = 0 # kg
        self.springForce = self.getSpringForce() # kg; calculates preload force on init
    
    def getForces(self,stroke):
        self.stroke = stroke
        self.getSpringForce()
        self.getGasForce()
        return self.springForce, self.gasForce
    
    def getSpringForce(self):
        preloadForce = self.preload*self.springRate*10*2 # multiply by 2 for both fork legs
        loadForce = self.stroke*self.springRate*10*2
        self.springForce = preloadForce+loadForce
        return self.springForce # kind of redundand to both set self.springForce and return it but makes funciton more versitile 
    
    def getGasForce(self):
        self.V2 = self.V1-(self.stroke*self.area)
        self.P2 = self.V1/self.V2*self.P1
        self.gasForce = (self.P2-self.atmPres)*self.area*2 # subtract atmPres to convert to gauge pressure; multiply by 2 for both fork legs
        return self.gasForce
    
    def forceSweep(self,E, B=0,step=.05):
        if E > self.airgap:
            print("***Error end stroke greater than airgap***")
        strokeIndex = []
        gasForce = []
        springForce = []
        combForce = []
        stroke = B
        while stroke <= E+.0001: #adding .0001 to E to remove float representation inaccuracies
            spring, gas = self.getForces(stroke)
            strokeIndex.append(stroke); springForce.append(spring); gasForce.append(gas); combForce.append(spring+gas)
            stroke += step
        return {"Stroke": strokeIndex, "Combined Force": combForce, "Spring Force": springForce, "Gas Force": gasForce}

class Simulate:
    # Methods to visualize data from ShockForce model 
    def get_data(self, simType="u",B=None, E=None,step=None):
        #If no args given then prompt user for simulation variables, otherwise run simulations using given variables
        simtType = simType.lower() # remove case sensitivity 
        if simType == "a":
            data = self.airgapSweep(B,E,step)
            print("Processing. This may take a minute...")
            anim = self.airgapAnimate(data)
        elif simType == "p":
            data = self.preloadSweep(B,E,step)
            print("Processing. This may take a minute...")
            anim = self.preloadAnimate(data)
        elif simType == "s":
            data = self.springRateSweep(B,E,step)
            print("Processing. This may take a minute...")
            anim = self.springRateAnimate(data)
        elif simType == "u":
            simType = input("Select simulation Type: (a)irgap sweep, (p)reload sweep, (s)pring rate sweep (a,p,s) ")
            if simType == "a":
                B = float(input("Smallest airgap modeled (cm): (>0.0-10.5) "))
                E = float(input("Largest airgap modeled (cm): (0.0-10.5) "))
                step = float(input("Increment airgap increased by (cm): (0.05-0.50 recommended) "))
            elif simType == "p":
                B = float(input("Lowest preload modeled (cm): (0.0-10.5) "))
                E = float(input("Greatest preload modeled (cm): (0.0-10.5) "))
                step = float(input("Increment preload increased by (cm): (0.05-0.50 recommended) "))
            elif simType == "s":
                B = float(input("Softest spring rate modeled (cm): (0.0-1.3 recommended) "))
                E = float(input("Firmest spring rate modeled (cm): (0.0-1.3 recommended) "))
                step = float(input("Increment sprin grate increased by (cm): (0.01-0.25 recommended) "))
            return self.get_data(simType,B,E,step)
        else:
            print("Error: unrecognized simulation type (simType) selected")
            return False
        jsAnim = anim.to_jshtml(default_mode="reflect") 
        self.saveAnimation(jsAnim)
        return HTML(jsAnim)
        
        
    def saveAnimation(self, jsAnim):
        savePrompt = input("Save model to disk, as HTML? (Select y if running outside of jupyter notebook) (y/n) ").lower()
        if savePrompt == "y":
            path = input("Path to save file: ")
            name = input("File name: ")
            if name[-5:].lower() !=".html":
                name +=".html"
            fullPath = join(path,name)
            try:
                with open(fullPath,"w") as f:
                    f.write(jsAnim)
                print("Save successful: %s " % fullPath)
            except:
                print("Error saving file at: %s" % fullPath)
                print("check save path and ensure you have permission to access destination folder.")
                self.saveAnimation(jsAnim)
        elif savePrompt == "n":
            pass
        else:
            self.saveAnimation(jsAnim)
                    
    def airgapSweep(self, B,E,step=0.5):
        if B <= 0:
            print("Error increase beginning airgap. It is too small to model")
            return False
        df = []
        airgap = E
        while airgap >= B:
            fork = ShockForce(4.1,airgap,.87)
            dataDict = fork.forceSweep(airgap,0,.01)
            plotDict = {"Spring Force": dataDict["Spring Force"], "Gas Force": dataDict["Gas Force"] }
            index = dataDict["Stroke"]
            df.append([airgap, pd.DataFrame(data=plotDict,index=index)])
            airgap -=step
        return df

    def preloadSweep(self, B,E,step=0.5):
        airgap = 10.5
        springRate = .87
        preload = E
        diameter = 4.1
        df  = []
        if B < 0 or B>=airgap:
            print("Error preload must be start must be above 0 or and end below %s" % (airgap))
            return False
        while preload >= B:
            fork = ShockForce(diameter,airgap,springRate,preload)
            dataDict = fork.forceSweep(10.5,0,.01)
            plotDict = {"Spring Force": dataDict["Spring Force"], "Gas Force": dataDict["Gas Force"] }
            index = dataDict["Stroke"]
            df.append([preload, pd.DataFrame(data=plotDict,index=index)]) #List of lists [preload,dataframe]
            preload -=step
        return df

    def springRateSweep(self, B,E,step=0.01):
        airgap = 10.5
        springRate = E
        preload = 0
        diameter = 4.1
        df  = []
        if B < 0 :
            print("Error - Spring Rate cannot be negative")
            return False
        while springRate >= B:
            fork = ShockForce(diameter,airgap,springRate,preload)
            dataDict = fork.forceSweep(10.5,0,.01)
            plotDict = {"Spring Force": dataDict["Spring Force"], "Gas Force": dataDict["Gas Force"] }
            index = dataDict["Stroke"]
            df.append([round(springRate,2), pd.DataFrame(data=plotDict,index=index)]) #List of lists [preload,dataframe]
            springRate -=step
        return df
    
    def airgapAnimate(self,data):
        xmax = data[0][1].index.max() # Max fork travel (used to set x axis)
        ymax = 800 # y axis max
        ims = [] # List of axes subplots
        fig, ax = plt.subplots()
        for airgap, df in data:
            ann = [] # List of annotations
            im = plt.stackplot(df.index, df["Spring Force"],df["Gas Force"], colors=("tab:blue","tab:orange")) #returns list of 2 polycollections
            title = "Air Gap: "+ str(round(airgap,1))+ " cm" # need to round due to float representation error
            ann.append(ax.annotate(text=title, xy=(xmax,ymax), verticalalignment='bottom', horizontalalignment='right', fontsize=17))
            ann.append(ax.annotate('Max Fork Travel ', fontsize=19, xy=(round(df.index[-1],2), ymax/2),  xycoords='data',
                    xytext=(int(xmax/2), ymax*7/8), textcoords='data',
                    arrowprops=dict(arrowstyle="simple, head_length=0.4,head_width=0.4, tail_width=0.1", shrinkA=15, shrinkB=0, facecolor="black"),
                    horizontalalignment='center', verticalalignment='top'))
            if airgap == data[0][0]: #If we're at first frame, so do formatting setup
                labels = list(df.columns)
                ax.legend(labels=labels, loc='upper left', fontsize=15)
                ax.set(ylim=(0,ymax), xlim=(0,xmax))
                ax.set_xlabel("Fork Compression (cm)", fontsize=17)
                ax.set_ylabel("Force (kg)", fontsize=17)
                ax.tick_params(axis='x', labelsize=15)
                ax.tick_params(axis='y', labelsize=15)
                fig.set_size_inches(10.66, 6)
            im.extend(ann)
            ims.append(im)
        anim = animation.ArtistAnimation(fig, ims, interval=20, blit=True)
        return anim
    
    def preloadAnimate(self,data):
        xmax = data[0][1].index.max() # Max fork travel (used to set x axis)
        ymax = 800 # y axis max
        ims = [] # List of axes subplots
        fig, ax = plt.subplots()
        for preload, df in data:
            ann = [] # List of annotations
            im = plt.stackplot(df.index, df["Spring Force"],df["Gas Force"], colors=("tab:blue","tab:orange")) #returns list of 2 polycollections
            preloadForce = df['Spring Force'].min() # Base preload force (ie spring force at 0cm compression)
            title = "Preload: "+ str(round(preload,1))+ " cm" # need to round due to float representation error
            ann.append(ax.annotate(text=title, xy=(xmax,ymax), verticalalignment='bottom', horizontalalignment='right', fontsize=17))
            ann.append(ax.axline((df.index[0], preloadForce), (df.index[-1], preloadForce), color="black"))
            ann.append(ax.annotate(text='Preload Force', fontsize=19, xy=(xmax/2,preloadForce),  xycoords='data',
                xytext=(xmax/2, ymax/2), textcoords='data',
                arrowprops=dict(arrowstyle="simple, head_length=0.4,head_width=0.4, tail_width=0.1", shrinkA=15, shrinkB=0, facecolor="black"),
                horizontalalignment='center', verticalalignment='top'))
            if preload == data[0][0]: #If we're at first frame, so do formatting setup
                labels = list(df.columns)
                ax.legend(handles=im, labels=labels, loc='upper left', fontsize=15) # Need to explicitly pass handles to avoid annotation lines (ann) showing up
                ax.set(ylim=(0,ymax), xlim=(0,xmax))
                ax.set_xlabel("Fork Compression (cm)", fontsize=17)
                ax.set_ylabel("Force (kg)", fontsize=17)
                ax.tick_params(axis='x', labelsize=15)
                ax.tick_params(axis='y', labelsize=15)
                fig.set_size_inches(10.66, 6)
            im.extend(ann)
            ims.append(im)
        anim = animation.ArtistAnimation(fig, ims, interval=20, blit=True)
        return anim
    
    def springRateAnimate(self,data):
        xmax = data[0][1].index.max() # Max fork travel (used to set x axis)
        ymax = 800 # y axis max
        ims = [] # List of axes subplots
        fig, ax = plt.subplots()
        for springRate, df in data:
            ann = [] # List of annotations
            im = plt.stackplot(df.index, df["Spring Force"],df["Gas Force"], colors=("tab:blue","tab:orange")) #returns list of 2 polycollections
            degrees_ = degrees(tan((df.iloc[300]["Spring Force"]-df.iloc[0]["Spring Force"])/(df.index[300]-df.index[0])*(xmax/ymax))) # the xmax/ymax normalizes with respect to x,y axis scales
            title = "Spring Rate: "+ str(round(springRate+.001,3))[:-1]+ " kg/mm" # need to round due to float representation error
            ann.append(ax.annotate(text=title, xy=(xmax,ymax), verticalalignment='bottom', horizontalalignment='right', fontsize=17))
            line1, = ax.plot((df.index[0], df.index[300]), 
                               (df.iloc[0]["Spring Force"],df.iloc[300]["Spring Force"]),
                               color="black") # hypotenuse note format here is (x1,x2 vals), (y1, y2 vals), also see line2 comment
            ann.append(line1) 
            line2, = ax.plot((df.index[0], df.index[300]), 
                               (df.iloc[0]["Spring Force"],df.iloc[0]["Spring Force"]), 
                               color="black") # Base, comma after line2 trick to return single Line2D primitive instead of container list 
            ann.append(line2) 
            ann.append(ax.annotate(text='', fontsize=19, xy=(df.index[300], df.iloc[300]["Spring Force"]),  xycoords='data',
                xytext=(df.index[300], df.iloc[0]["Spring Force"]), textcoords='data',
                arrowprops=dict(arrowstyle="simple, head_length=0.3,head_width=0.3, tail_width=0.05", connectionstyle="arc3,rad=.3", shrinkA=0, shrinkB=0, facecolor="black"),
                horizontalalignment='center', verticalalignment='top')) # Curvy Arrow
            ann.append(ax.text(df.index[325], data[0][1].iloc[150]["Spring Force"], str(round(degrees_))+"°", 
                               fontsize=19, verticalalignment='center', horizontalalignment='left')) # Text position fixed, but value is not, y pos is not.  Hence y pos set by first item in data list (greatest springrate)
            if springRate == data[0][0]: #If we're at first frame, so do formatting setup
                labels = list(df.columns)
                ax.legend(handles=im, labels=labels, loc='upper left', fontsize=15) # Need to explicitly pass handles to avoid annotation lines (ann) showing up
                ax.set(ylim=(0,ymax), xlim=(0,xmax))
                ax.set_xlabel("Fork Compression (cm)", fontsize=17)
                ax.set_ylabel("Force (kg)", fontsize=17)
                ax.tick_params(axis='x', labelsize=15)
                ax.tick_params(axis='y', labelsize=15)
                fig.set_size_inches(10.66, 6)
            im.extend(ann)
            ims.append(im)
        anim = animation.ArtistAnimation(fig, ims, interval=20, blit=True)
        return anim

sim = Simulate()
sim.get_data()
#Examples of directly passing on paramaters without user prompt
#s = sim.get_data('s',0,1.3,.01)
#p = sim.get_data('p',0,10.5,.05)
#a = sim.get_data('a',0.05,10.5,.05)
