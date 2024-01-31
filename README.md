# Recipes for eccentricity reduction of DNS data with Sgrid and BAM or Cactus

## There are 2 ways to reduce eccentricity:

## 1. Run sgrid with:
DNSdata_adjust = forcebalance always
With this sgrid adjusts DNSdata_Omega at every iteration using the force
balance equation.
In this case we need the script [EccRed.py](EccRed.py)

## 2. Run sgrid with:
DNSdata_adjust = Py0
With this sgrid keeps DNSdata_Omega fixed to whatever we specify in its
parfile.
In this case we need the script [EccRed_noForceBal.py](EccRed_noForceBal.py)

## Additional information:

The 2nd way is recommended for low eccentricities unless the mass ratio
is high. The 2nd way is described in
[EccRed_v2.md](https://github.com/sgridsource/EccRed/blob/main/EccRed_v2.md)

Additional details about the 2 ways are in
[Ecc-Red-Notes.txt](Ecc-Red-Notes.txt). For either way
we need scripts to fit the orbital separation to the sinusoidal curve
d(t) = S0 + A0 t + 0.5 A1 t^2 - (B/omega) cos(omega t + phi).

For the 1st way we have EccRed.py (see e-based eccentricity reduction in
[1507.07100](https://arxiv.org/abs/1507.07100)).
For the 2nd way we use EccRed_noForceBal.py (see Omega-based eccentricity
reduction in [1910.09690](https://arxiv.org/abs/1910.09690)).

To check that the fit was successful, one needs to plot the fit and the
original data. This can be done with
[tgraph](https://github.com/wofti/tgraph).
