# ShockForce
### OVERVIEW
This program models the static forces of a motorcycle front suspension.  This is intended as a tool to both educate and inform riders how common, easily changed paramaters affect a motorcycle suspension.  This is achieved through rendering a series of graphs where a single paramater is changed in linear space and assembling them into an animation.  The user interface was created using Qt (pyQt5) and the data visualization with Matplotlib.  The data itself is calculated by a "homespun" class using a methodology described below.

<div align="center"><img src=https://user-images.githubusercontent.com/87097441/126754682-3edc998d-a5c7-4963-a1f2-11302277080a.jpg width="700" height="auto"/></div>

### EXAMPLES
<div align="center">
<i><b>*** Click each chart to open an interactive animation -- These are previews ***</b></i> 
</div>

<table>
    <tr>
        <th><a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/airgap.html><img src=https://user-images.githubusercontent.com/87097441/124851501-81eeed00-df57-11eb-8caf-3ec4f25d9536.gif alt="Air gap animation" height="auto" width="475" /></a></th>
        <th><a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/preload.html> <img src=https://user-images.githubusercontent.com/87097441/124851507-85827400-df57-11eb-9aae-0cd5bf845540.gif alt="Preload animation" height="auto" width="475"/></a></th>
    </tr>
    <tr>
        <th>Airgap sweep from 0 to 10.5 cm in 0.05 cm increments</th>
        <th>Airgap sweep from 0 to 10.5 cm in 0.05 cm increments</th>
    </tr>
    <tr>
        <th colspan=2><a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/springrate.html> <img src=https://user-images.githubusercontent.com/87097441/124851515-887d6480-df57-11eb-964a-68bdb8243d65.gif alt="Spring rate animation" height="auto" width="475"/></a></th>
    </tr>
    <tr>
        <th colspan=2>Spring rate sweep from 0 to 1.3 kg/mm in 0.01 kg/mm increments</th>
    </tr>
</table>

### METHODOLOGY
* The geometry of the fork is based around a 2015 Yamaha FZ-07, but general trends should apply to all motorcycles with damper rod forks.
* Only static forces are modeled.  Dynamic forces (shock damping) are not modeled.
* Static forces are broken down into:
  1. Spring Forces:
      * Modeled as an ideal spring (spring rate: 0.87 kg/mm, unless otherwise specified)
  2. Gas Forces:
      * Calculated using ideal gas law.  These forces arise from isothermal compression of air in the headspace as the fork (motorcycle front suspension) compresses.
* For the variable being modeled (air gap, spring preload or spring rate), ShockForce sweeps through a range of values, traveling from user specified beginning to end values in user defined increments.  For each variable value in the sweep, the forces across the full range of fork travel are modeled.

