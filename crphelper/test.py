from crphelper import functions
import pandas as pd

# Please replace path with your own path for CRPropa data before using.
path = "sim3d-G12-100-E_1e+14eV-D_8.5e+02Mpc-B_1e-15G-Lc_1e-03Mpc-nB_2.00-nEvents_100000.txt"
df = pd.read_csv(path, skiprows=14, sep='\t',  lineterminator='\n', header=None)
df = df[df.iloc[:,3] == 22] # photons

e = functions.extract_e(df)

# spectrum(data, nbins=10000, include_normal=False)
functions.spectrum(e)

# corr_length(lmin, lmax, nB=-5/3)
print(functions.corr_length(60, 800)) #384.0292879205956

# find_lmax(lc, lmin, nB=-5/3)
print(functions.find_lmax(384, 60)) #799.930535164668

# extension_angles(df, print_average=True)
# returns angles in degrees; prints average angle
theta = functions.extension_angles(df)

# deflection_angles(df, print_average=True)
delta = functions.deflection_angles(df)

# plot_angles(df, angles, plot_binned=True, plot_hist=True)
# plot_binned: plot average angle binned by the particles' energies
# plot_hist: plot histogram of all angles
functions.plot_angles(df, theta)
functions.plot_angles(df, delta)
