## Spectral Response Functions
### Spectral Response functions
#Py6S uses the Wavelength class to handle the wavelength(s) associated with a given channel (a.k.a. waveband). This might be a single scalar value (e.g. a central wavelength) or, if known, possibly the spectral response function of the waveband. The Sentinel 2 spectral response functions are provided with Py6S (as well as those of a number of missions). For more details please see the [docs](http://py6s.readthedocs.io/en/latest/params.html#wavelengths) or the (comment-rich) [source code](https://github.com/robintw/Py6S/blob/master/Py6S/Params/wavelength.py)

def spectralResponseFunction(bandname):
    """
    Extract spectral response function for given band name
    """
    bandSelect = {
        'B1':PredefinedWavelengths.S2A_MSI_01,
        'B2':PredefinedWavelengths.S2A_MSI_02,
        'B3':PredefinedWavelengths.S2A_MSI_03,
        'B4':PredefinedWavelengths.S2A_MSI_04,
        'B5':PredefinedWavelengths.S2A_MSI_05,
        'B6':PredefinedWavelengths.S2A_MSI_06,
        'B7':PredefinedWavelengths.S2A_MSI_07,
        'B8':PredefinedWavelengths.S2A_MSI_08,
        'B8A':PredefinedWavelengths.S2A_MSI_09,
        'B9':PredefinedWavelengths.S2A_MSI_10,
        'B10':PredefinedWavelengths.S2A_MSI_11,
        'B11':PredefinedWavelengths.S2A_MSI_12,
        'B12':PredefinedWavelengths.S2A_MSI_13,
        }
    return Wavelength(bandSelect[bandname])



### TOA Reflectance to Radiance
#Sentinel 2 data is provided as top-of-atmosphere reflectance. Lets convert this to at-sensor radiance for the atmospheric correction.*
#\*<sub>You *can* atmospherically corrected directly from TOA reflectance. However, I suggest radiance for a couple of reasons.
#  Firstly, it is more intuitive. Instead of *spherical albedo* (which I suspect is more of a mathematical convenience than a physical property) you can use solar irradiance, transmissivity, path radiance, etc. Secondly, Py6S seems to be more geared towards converting from radiance to SR</sup>

def toa_to_rad(bandname):
    """
    Converts top of atmosphere reflectance to at-sensor radiance
    """
    # solar exoatmospheric spectral irradiance
    ESUN = info['SOLAR_IRRADIANCE_'+bandname]
    solar_angle_correction = math.cos(math.radians(solar_z))
    # Earth-Sun distance (from day of year)
    doy = scene_date.timetuple().tm_yday
    d = 1 - 0.01672 * math.cos(0.9856 * (doy-4))# http://physics.stackexchange.com/questions/177949/earth-sun-distance-on-a-given-day-of-the-year
    # conversion factor
    multiplier = ESUN*solar_angle_correction/(math.pi*d**2)
    # at-sensor radiance
    rad = toa.select(bandname).multiply(multiplier)
    return rad

### Radiance to Surface Reflectance

#Reflected sunlight can be described as follows (wavelength dependence is implied):
#$ L = \tau\rho(E_{dir} + E_{dif})/\pi + L_p$
#where L is at-sensor radiance, $\tau$ is transmissivity, $\rho$ is surface reflectance, $E_{dir}$ is direct solar irradiance, $E_{dif}$ is diffuse solar irradiance and $L_p$ is path radiance. There are five unknowns in this equation, 4 atmospheric terms ($\tau$, $E_{dir}$, $E_{dif}$ and $L_p$) and surface reflectance. The 6S radiative transfer code is used to solve for the atmospheric terms, allowing us to solve for surface reflectance.
#$ \rho = \pi(L - L_p) / \tau(E_{dir} + E_{dif}) $

def surface_reflectance(bandname):
    """
    Calculate surface reflectance from at-sensor radiance given waveband name
    """
    # run 6S for this waveband
    s.wavelength = spectralResponseFunction(bandname)
    s.run()
    # extract 6S outputs
    Edir = s.outputs.direct_solar_irradiance             #direct solar irradiance
    Edif = s.outputs.diffuse_solar_irradiance            #diffuse solar irradiance
    Lp   = s.outputs.atmospheric_intrinsic_radiance      #path radiance
    absorb  = s.outputs.trans['global_gas'].upward       #absorption transmissivity
    scatter = s.outputs.trans['total_scattering'].upward #scattering transmissivity
    tau2 = absorb*scatter                                #total transmissivity
    # radiance to surface reflectance
    rad = toa_to_rad(bandname)
    ref = rad.subtract(Lp).multiply(math.pi).divide(tau2*(Edir+Edif))
    return ref