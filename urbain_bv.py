# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:10:00 2022

@author: Geo
"""
#variables    
import qgis 
bvTotal=QgsProject.instance().mapLayersByName('bassin_versant_topographique_calcul')[0]
urbain = QgsProject.instance().mapLayersByName('batiment_bdtopo_ign2021')[0]
masseEau = QgsProject.instance().mapLayersByName('MasseDEauCotiere_MYT2019-shp MasseDEauCotiere_MYT')[0]


# définition nouveaux champ pour la couche route
surfaceBati = QgsField("surface_batiment", QVariant.Double)

#ajout nouveaux champs dans la couche urbain
urbain.dataProvider().addAttributes([surfaceBati])
urbain.updateFields()
print ([f.name() for f in urbain.fields()])

#calcul surface batiment
import time
start_time = time.time()
with edit(urbain):
    ##start an undo block
    urbain.beginEditCommand('mise a jour berme')
    for f in urbain.getFeatures():
            geom = f.geometry()
            f['surface_batiment'] = geom.area()
            urbain.updateFeature(f)
##fin undo block
    urbain.endEditCommand()
    end_time = time.time()
    print(f"Temps calcul surface bati : {end_time-start_time}") 

# Set properties for the join
bvJointure='cleabs'

#calcul intersection bv et urbain 
import time
start_time = time.time()
        ##start an undo block
bvTotal.beginEditCommand('')    
bvTotalUrbain = processing.runAndLoadResults("native:intersection", {'INPUT':bvTotal,
    'OVERLAY':urbain,
    'INPUT_FIELDS':['cleabs','code_hydrographique', 'toponyme','code_bdcarthage', 'liens_vers_cours_d_eau_principa'],
    'OVERLAY_FIELDS':['surface_batiment'],
    'OVERLAY_FIELDS_PREFIX':'',
    'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
##fin undo block
bvTotal.endEditCommand()
end_time = time.time()
print(f"Temps intersection bv et urbain : {end_time-start_time}")

    # aggréger champ surface urbain par bv
surfaceUrbainBv = processing.runAndLoadResults("native:aggregate", {
    'INPUT':bvTotalUrbain,
    'GROUP_BY':bvJointure,
    'AGGREGATES':[{'aggregate': 'concatenate_unique','delimiter': ',','input': bvJointure,'length': 24,'name': bvJointure,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
                  {'aggregate': 'sum','delimiter': ',','input': '"surface_batiment"','length': 0,'name': 'surface_batiment','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
print("l'aggrégation de la surface des bâtis par bv est réussie")

#jointure couche calcul surface urbain à la couche bv
bvTotalUrbainSomme = processing.runAndLoadResults("native:joinattributestable", {
    'INPUT':bvTotal,
    'FIELD':bvJointure,
    'INPUT_2':surfaceUrbainBv,
    'FIELD_2':bvJointure,
    'FIELDS_TO_COPY':['fid','surface_batiment'],
    'METHOD':0,'DISCARD_NONMATCHING':False,
    'PREFIX':'','OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
print("la jointure surface bati à la couche bv est réussie")

#joindre par localisation bv par masse d'eau cotière'
bvMasseEau = processing.runAndLoadResults("native:joinattributesbylocation", {
    'INPUT':bvTotalUrbainSomme,
    'PREDICATE':[0],'JOIN':masseEau,
    'JOIN_FIELDS':['CdEuMasseD','NomMasseDE','TypeMasseD','SurfaceTot'],'METHOD':0,'DISCARD_NONMATCHING':False,'PREFIX':'masseEauCotiere_','OUTPUT':'TEMPORARY_OUTPUT'})
print("Succès pour la jointure spatiale des bv avec les masse d'eau cotière")
print("il faut supprimer manuellement les connections bv & masse d'eau non connectées (voir carte)")


# définition nouveaux champ pour la couche bv
surfaceBV = QgsField("surface_bv", QVariant.Double)

bvMasseEau = iface.activeLayer()
#ajout nouveaux champs dans la couche urbain
bvMasseEau.dataProvider().addAttributes([surfaceBV])
bvMasseEau.updateFields()
print ([f.name() for f in bvMasseEau.fields()])

#calcul surface bv
import time
start_time = time.time()
with edit(bvMasseEau):
    ##start an undo block
    bvMasseEau.beginEditCommand('mise a jour berme')
    for f in bvMasseEau.getFeatures():
            geom = f.geometry()
            f['surface_bv'] = geom.area()
            bvMasseEau.updateFeature(f)
##fin undo block
    bvMasseEau.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 
QgsProject.instance().addMapLayer(bvMasseEau)    