# shockForce
### OVERVIEW
This is a collection of methods that models the static forces of a motorcycle front fork (suspension).  The intent is to visualize how changes to air gap, spring preload and spring rate affect a motorcycle suspension. shockForce generates graphic animations using matplotlib, allowing changes to the aforementioned variables to be visualized. 

### METHODOLOGY
* The geometry of the fork is based around a 2015 Yamaha FZ-07, but general trends should apply to all motorcycles with damper rod forks.
* Only static forces are modeled.  Dynamic forces (shock damping) are not modeled.
* Static forces are broken down into:
  1. Spring forces:
      * Modeled as an ideal spring (spring rate 0.87 kg/mm, unless otherwise specified)
  2. Gas Forces:
      * Calculated using ideal gas law.  These forces arise from isothermal compression of air in the headspace as the fork (motorcycle front suspension) compresses.
* For the variable being modeled (air gap, spring preload or spring rate), gas force sweeps through a range of values, traveling from user specified beginning to end values in user defined increments.  For each variable value in the sweep, the forces across the full range of suspension travel are modeled.
