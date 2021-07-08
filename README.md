# ShockForce
### OVERVIEW
This program models the static forces of a motorcycle front fork (suspension).  The intent is to visualize how changes to the variables: air gap, spring preload and spring rate affect a motorcycle suspension. ShockForce generates graphic animations using matplotlib, allowing changes to the aforementioned variables to be visualized. 

### EXAMPLES

<p align="center">
<i><b>*** Click each chart to open an interactive animation -- These are previews ***</b></i> 
</p>

<p align="center">
  <a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/airgap.html>
  <img src=https://user-images.githubusercontent.com/87097441/124851501-81eeed00-df57-11eb-8caf-3ec4f25d9536.gif alt="Air gap animation"></a><br>
  <b>Airgap sweep from 0 to 10.5 cm in 0.05 cm increments</b><br>
</p>

<p align="center">
  <a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/preload.html>
  <img src=https://user-images.githubusercontent.com/87097441/124851507-85827400-df57-11eb-9aae-0cd5bf845540.gif alt="Preload animation"></a><br>
  <b>Spring preload sweep from 0.05 to 10.5 cm in 0.05 cm increments</b><br>
</p>

<p align="center">
  <a href=https://htmlpreview.github.io/?https://github.com/ericghara/ShockForce/blob/main/examples/springrate.html>
  <img src=https://user-images.githubusercontent.com/87097441/124851515-887d6480-df57-11eb-964a-68bdb8243d65.gif alt="Spring rate animation"></a><br>
  <b>Spring rate sweep from 0 to 1.3 kg/mm in 0.01 kg/mm increments</b><br>
</p>

### METHODOLOGY
* The geometry of the fork is based around a 2015 Yamaha FZ-07, but general trends should apply to all motorcycles with damper rod forks.
* Only static forces are modeled.  Dynamic forces (shock damping) are not modeled.
* Static forces are broken down into:
  1. Spring Forces:
      * Modeled as an ideal spring (spring rate: 0.87 kg/mm, unless otherwise specified)
  2. Gas Forces:
      * Calculated using ideal gas law.  These forces arise from isothermal compression of air in the headspace as the fork (motorcycle front suspension) compresses.
* For the variable being modeled (air gap, spring preload or spring rate), ShockForce sweeps through a range of values, traveling from user specified beginning to end values in user defined increments.  For each variable value in the sweep, the forces across the full range of suspension travel are modeled.

