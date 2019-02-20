carcasslocs <-read.delim("/home/maya/Downloads/REINDEERLOCS.txt",sep=';')
xy <- carcasslocs[,c(3,4)]

library(rgdal);library(sp)
spdf <- SpatialPointsDataFrame(coords = carcasslocs[,c(3,4)], data = carcasslocs,
                               proj4string = CRS("+init=epsg:32632"))
carclocsTransformed <-  spTransform(spdf, CRS("+init=epsg:4326"))

coordinates(carclocsTransformed)
writeOGR(carclocsTransformed["coords"], "carclocs.kml", layer="FID", driver="KML") 
writeOGR(carclocsTransformed, dsn="carclocs.kml", layer= "FID", driver="KML")
