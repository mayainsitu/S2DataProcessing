from IPython.display import display, Image
import math

"""
All functions below have been derived from Sam Murphy's git repository
https://github.com/mayastn/cloud-masking-sentinel2.git
"""

def rescale(img, thresholds):
    """
    Linear stretch of image between two threshold values.
    """
    return img.subtract(thresholds[0]).divide(thresholds[1] - thresholds[0])


def sentinelCloudScore(img):
    """
    Computes spectral indices of cloudyness and take the minimum of them.
    Each spectral index is fairly lenient because the group minimum
    is a somewhat stringent comparison policy. side note -> this seems like a job for machine learning :)
    originally written by Matt Hancher for Landsat imagery
    adapted to Sentinel by Chris Hewig and Ian Housman
    """
    # cloud until proven otherwise
    score = ee.Image(1)
    # clouds are reasonably bright
    score = score.min(rescale(img.select(['blue']), [0.1, 0.5]))
    score = score.min(rescale(img.select(['aerosol']), [0.1, 0.3]))
    score = score.min(rescale(img.select(['aerosol']).add(img.select(['cirrus'])), [0.15, 0.2]))
    score = score.min(rescale(img.select(['red']).add(img.select(['green'])).add(img.select('blue')), [0.2, 0.8]))
    # clouds are moist
    ndmi = img.normalizedDifference(['red4','swir1'])
    score=score.min(rescale(ndmi, [-0.1, 0.1]))
    # clouds are not snow.
    ndsi = img.normalizedDifference(['green', 'swir1'])
    score=score.min(rescale(ndsi, [0.8, 0.6])).rename(['cloudScore'])
    return img.addBands(score)


def ESAcloudMask(img):
    """
    European Space Agency (ESA) clouds from 'QA60', i.e. Quality Assessment band at 60m
    parsed by Nick Clinton
    """
    qa = img.select('QA60')
    # bits 10 and 11 are clouds and cirrus
    cloudBitMask = int(2**10)
    cirrusBitMask = int(2**11)
    # both flags set to zero indicates clear conditions.
    clear = qa.bitwiseAnd(cloudBitMask).eq(0).And(\
           qa.bitwiseAnd(cirrusBitMask).eq(0))
    # clouds is not clear
    cloud = clear.Not().rename(['ESA_clouds'])
    # return the masked and scaled data.
    return img.addBands(cloud)


def shadowMask(img,cloudMaskType):
    """
    Finds cloud shadows in images
    Originally by Gennadii Donchyts, adapted by Ian Housman
    """
    def potentialShadow(cloudHeight):
        """
        Finds potential shadow areas from array of cloud heights
        returns an image stack (i.e. list of images)
        """
        cloudHeight = ee.Number(cloudHeight)
        # shadow vector length
        shadowVector = zenith.tan().multiply(cloudHeight)
        # x and y components of shadow vector length
        x = azimuth.cos().multiply(shadowVector).divide(nominalScale).round()
        y = azimuth.sin().multiply(shadowVector).divide(nominalScale).round()
        # affine translation of clouds
        cloudShift = cloudMask.changeProj(cloudMask.projection(), cloudMask.projection().translate(x, y)) # could incorporate shadow stretch?
        return cloudShift
    # select a cloud mask
    cloudMask = img.select(cloudMaskType)
    # make sure it is binary (i.e. apply threshold to cloud score)
    cloudScoreThreshold = 0.5
    cloudMask = cloudMask.gt(cloudScoreThreshold)
    # solar geometry (radians)
    azimuth = ee.Number(img.get('solar_azimuth')).multiply(math.pi).divide(180.0).add(ee.Number(0.5).multiply(math.pi))
    zenith  = ee.Number(0.5).multiply(math.pi ).subtract(ee.Number(img.get('solar_zenith')).multiply(math.pi).divide(180.0))
    # find potential shadow areas based on cloud and solar geometry
    nominalScale = cloudMask.projection().nominalScale()
    cloudHeights = ee.List.sequence(500,4000,500)
    potentialShadowStack = cloudHeights.map(potentialShadow)
    potentialShadow = ee.ImageCollection.fromImages(potentialShadowStack).max()
    # shadows are not clouds
    potentialShadow = potentialShadow.And(cloudMask.Not())
    # (modified) dark pixel detection
    darkPixels = toa.normalizedDifference(['green', 'swir2']).gt(0.25)
    # shadows are dark
    shadows = potentialShadow.And(darkPixels).rename(['shadows'])
    # might be scope for one last check here. Dark surfaces (e.g. water, basalt, etc.) cause shadow commission errors.
    # perhaps using a NDWI (e.g. green and nir)
    return img.addBands(shadows)


def quicklook(bandNames, mn, mx, region, gamma=False, title=False):
    """
    Displays images in notebook
    """
    if title:
        print('\n',title)
    if not gamma:
        gamma = 1
    visual = Image(url=toa.select(bandNames).getThumbUrl({
                'region':region,
                'min':mn,
                'max':mx,
                'gamma':gamma,
                'title':title
                }))
    display(visual)
