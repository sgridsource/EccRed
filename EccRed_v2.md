# Eccentricity Reduction Algorithm (using rdot and Omega)

## Introduction
When we construct quasi-equilibrium initial data for binary neutron stars
(BNS) and then evolve them to simulate the BNS system, the orbits deviate
from perfect inspiral orbits in that the distance is not decreasing with a
steeper and steeper slope, in other words, the orbits are eccentric.
If we desire high precision orbits and gravitational waves we need to
reduce this eccentricity as much as possible by figuring out the correct
values of the radial velocity rdot and the orbital angular velocity Omega
in the initial data.

More info about the old version of the eccentricity reduction procedure (in
EccRed.py) is in https://arxiv.org/pdf/1507.07100.pdf. The new procedure
is in the paper about the new SGRID version https://arxiv.org/abs/1910.09690.

### Requirements:
* New version of SGRID code (DNSdata)
* SGRID parameter file
* SGRID parfile needs to have: `DNSdata_adjust = Py0`
* BAM code
* BAM parameter file
* Python script **EccRed_noForceBal.py**


### Algorithm

While eccentricity less than a desired value do steps 1-5:


> *Step 1: Run SGRID*

Construct initial data by running SGRID for the given parameter
file. Let's say the name of the SGRID parameter file is **bns.par**.

>> **IF** this is the very first step of SGRID run we need to set the two
parameters `DNSdata_rdot` and `DNSdata_Omega`. `DNSdata_rdot` can be set to
0, or to the value of a previous similar simulation.
`DNSdata_Omega` can be set to a post-Newtonian estimate i.e.
`DNSdata_Omega = estimate`, or to the value of a previous similar simulation.
For example, we can start with the following parameters:

```
DNSdata_rdot = 0
DNSdata_Omega = estimate
```


> *Step 2: Modify the SGRID output*

SGRID runs different resolutions to make initial date and for
the evolution we will use the highest resolution.
The naming convention for the output directory for each resolution
is `parameterfile_n1_n2_n3`. Thus, if our parameter file is
`bns.par` and the highest resolution is 26x26x26 we will have:
`bns_26_26_26`.

In order to evolve the initial data using the BAM code we need to do
the following modification:

* Copy `bns.par` to `bns_26_26_26/bns_26_26_26.par`.
* Open `bns_26_26_26/bns_26_26_26.par` and change
  `iterate_parameters = yes` to `iterate_parameters = no`.


> *Step 3: Run BAM code*

Evolve the system using the newly constructed initial data for about 3 orbits.
There are few caveats worth noting:

* The parameter `BNSdataReader_sgrid_exe` must be set to the path of the
  SGRID executable.
* The parameter `BNSdataReader_sgrid_datadir` must be set to the path of
  the highest resolution of the SGRID output, in our case the path of
  `bns_26_26_26` folder.
* The parameter `eos_tab_file` must be set to the correct table
  containing the same equation of state as used by SGRID.
* Make sure the finest level of BAM's mesh is big enough to
  fit the entire star diameter plus an extra 10 percent.
  One can find the diameter of each star by '|xin-xout|'.
  The values of `xin` and `xout` are at the file `BNSdata_properties.txt`
  in `bns_26_26_26` folder.


> *Step 4: Find changes in radial velocity and orbital angular velocity*

One can use the provided python script *EccRed_noForceBal.py* to
find the changes we need to make in the SGRID parameters `DNSdata_rdot`
and `DNSdata_Omega`. This script fits the distance versus time to a simple
curve. From the curve fit parameters the changes in `DNSdata_rdot`
and `DNSdata_Omega` are then computed. We invoke the script as follows:

`EccRed_noForceBal.py --Mass MASS --Omega OMEGA --tskip TIMESKIP --dmin D_MIN moving_puncture_distance.lxyz4 > fit.data`

The values of `MASS`, `OMEGA`, `TIMESKIP` and `D_MIN` are found as follows:

* The values of `OMEGA` and `MASS` are equal to the values of `Omega` and
  `M_ADM` in `BNSdata_properties.txt` located in `bns_26_26_26` folder.
* To find the values of `TIMESKIP` and `D_MIN` we need to first Plot
  `d-proper` versus `time` in `moving_puncture_distance.lxyz?` located in the
  BAM output directory. Looking at the plot we observe that there are some
  wiggles at the early times. Find when these wiggles end, this time
  is the value of `TIMESKIP`. Furthermore, find the smallest `d-proper`
  that we want to include into the fit, this gives the value of `D_MIN`.

After invoking the script we need to double check the fit results. These are
in the file `fit.data`. The 1st column contains time, the 2nd distance
and the 3rd the fit to the distance. To check the fit quality, plot both
column 2 versus 1 as well as column 3 versus 1:

`tgraph.py -c 1:2 fit.data -c 1:3 fit.data`

Make sure the 2nd curve is a good fit to the first.
(tgraph is at https://github.com/wofti/tgraph)

Now, **to find the changes in `DNSdata_rdot` and `DNSdata_Omega`**,
go the the tail of the file `fit.data` and read the value of `drdot` and
`dOmega` under the `Best Results` header. The value of `ecc` represents the
current measured eccentricity of the simulation.


> *Step 5: Update SGRID parameter file*

Having found `drdot` and `dOmega`, add these two values to the current
values of `DNSdata_rdot` and `DNSdata_Omega` (the value of DNSdata_Omega can
be found in BNSdata_properties.txt) to obtain the SGRID parameters for the
next iteration.
