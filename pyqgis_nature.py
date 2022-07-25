#bv1 total
#bvTotal=QgsProject.instance().mapLayersByName('bassin_versant_topographique')[0]
#dupliquer données source
bvTotal=QgsProject.instance().mapLayersByName('bassin_versant_topographique_calcul')[0]
foretTotal=QgsProject.instance().mapLayersByName('')[0]
sportTotal=QgsProject.instance().mapLayersByName('')[0]
cimetiereTotal=QgsProject.instance().mapLayersByName('')[0]
natureListe = [bv, foret, football, cimetiere]

# Set champ de jointure for the join, 
bvJoin ='cleabs'



##ajout champ surface
#surface = QgsField("surface", QVariant.Double)
#s2.dataProvider().addAttributes([surface])
#s2.updateFields()
#s1.dataProvider().addAttributes([surface])
#s1.updateFields()

#
##calcul champ surface
#with edit(s1):
#    s1.beginEditCommand('mise à jour surface')
#    for f in s1.getFeatures():
#        geom= f.geometry()
#        f['surface'] = geom.area()
#        s1.updateFeature(f)
#    s1.endEditCommand()    
#
 
iface.showAttributeTable(sp1)
QgsProject.instance().addMapLayer(bv1nature)




    # aggréger champ surface foret par bv
for i in range(len(nature)):
    foretBv = processing.run("native:aggregate", {
    'INPUT':foretTotal,
    'GROUP_BY':bvJoin,
    'AGGREGATES':[{
    'aggregate': 'concatenate_unique','delimiter': ',','input':bvTotal,'length': 24,'name': bvTotal,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
    {'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

# calcul de la surface de type de nature pour chaque bassin versant et aggrégation des données entre elles
'INPUT':foretTotal,
'GROUP_BY':bvJoin,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input':bvTotal,'length': 24,'name': bvTotal,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']


sp1 = processing.run("native:aggregate", {
'INPUT':s1,
'GROUP_BY':bvJoin,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input': bvTotal,'length': 24,'name': bvTotal,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

ci1 = processing.run("native:aggregate", {
'INPUT':c1,
'GROUP_BY':bvJoin,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input': bvTotal,'length': 24,'name': bvTotal,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

for2 = processing.run("native:aggregate", {
'INPUT':f2,
'GROUP_BY':bv2f,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input':bv2f,'length': 24,'name': bv2f,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

sp2 = processing.run("native:aggregate", {
'INPUT':s2,
'GROUP_BY':bv2f,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input': bv2f,'length': 24,'name': bv2f,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']


ci2 = processing.run("native:aggregate", {
'INPUT':c2,
'GROUP_BY':bv2f,
'AGGREGATES':[{
'aggregate': 'concatenate_unique','delimiter': ',','input': bv2f,'length': 24,'name': bv2f,'precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},
{'aggregate': 'sum','delimiter': ',','input': '"surface"','length': 0,'name': 'surface','precision': 0,'sub_type': 0,'type': 6,'type_name': 'double precision'}],'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

#ajout au bv données sport
bv1sport = processing.run("native:joinattributestable", {
'INPUT':bv1,
'FIELD':bvJoin,
'INPUT_2':sp1,
'FIELD_2':bvJoin,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'football_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

#ajout données foret
bv1foret = processing.run("native:joinattributestable", {
'INPUT':bv1sport,'FIELD':bvJoin,
'INPUT_2':for1,'FIELD_2':bvJoin,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'foret_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
#ajout données cimetière
bv1nature = processing.run("native:joinattributestable", {
'INPUT':bv1foret,
'FIELD':bvJoin,
'INPUT_2':ci1,
'FIELD_2':bvJoin,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'cimetiere_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

#ajout données sport
bv2sport = processing.run("native:joinattributestable", {
'INPUT':bv2,
'FIELD':bv2f,
'INPUT_2':sp2,
'FIELD_2':bv2f,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'football_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT'] 
#ajout données foret
bv2foret = processing.run("native:joinattributestable", {
'INPUT':bv2sport,
'FIELD':bv2f,
'INPUT_2':for2,
'FIELD_2':bv2f,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'foret_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
#ajout données cimetière
bv2nature = processing.run("native:joinattributestable", {
'INPUT':bv2foret,
'FIELD':bv2f,
'INPUT_2':ci2,
'FIELD_2':bv2f,
'FIELDS_TO_COPY':['surface'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'cimetiere_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

# ajout nouveau champ (somme surface bat terrain et route)
# définition du champ à créer
surface = QgsField("surface", QVariant.Double)
sururb = QgsField("surface_nature", QVariant.Double)
poururb = QgsField("pourc_nature", QVariant.Double)

##ajout champ
bv1nature.dataProvider().addAttributes([surface, sururb,poururb])
#mise à jour des champs dans la couche
bv1nature.updateFields()
bv2nature.dataProvider().addAttributes([surface, sururb,poururb])
#mise à jour des champs dans la couche
bv2nature.updateFields()
##remplacer null par 0
import time
start_time = time.time()
with edit(bv1nature):
        ##start an undo block
    bv1nature.beginEditCommand('mise a jour berme')
    for f in bv1nature.getFeatures():
        attributes = f.attributes()
        new_attributes = [a or 0 for a in attributes]
        f.setAttributes(new_attributes)
        bv1nature.updateFeature(f)
        ##fin undo block
    bv1nature.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

import time
start_time = time.time()
with edit(bv2nature):
        ##start an undo block
    bv2nature.beginEditCommand('mise a jour berme')
    for f in bv2nature.getFeatures():
        attributes = f.attributes()
        new_attributes = [a or 0 for a in attributes]
        f.setAttributes(new_attributes)
        bv2nature.updateFeature(f)
        ##fin undo block
    bv2nature.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

# calcul surface urbain
surUrb = QgsExpression('football_surface + foret_surface + cimetiere_surface')
pourUrb = QgsExpression('surface_nature/ surface * 100')
#expression à calculer et définition variable
##To execute our expressions, we need to provide an appropriate QgsExpressionContext. To set it up, use:
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(bv1nature)

##calcul surface (à lancer au fur et à mesure)
import time
start_time = time.time()
with edit(bv1nature):
    ##start an undo block
    bv1nature.beginEditCommand('mise a jour berme')
    for f in bv1nature.getFeatures():
            context.setFeature(f)
            f['surface_nature'] = surUrb.evaluate(context)
            bv1nature.updateFeature(f)
    for f in bv1nature.getFeatures():
            geom = f.geometry()
            f['surface'] = geom.area()
            bv1nature.updateFeature(f)
            context.setFeature(f)
            f['pourc_nature'] = pourUrb.evaluate(context)
            bv1nature.updateFeature(f)
##fin undo block
    bv1nature.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}")     
    
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(bv2nature)
##largeur chaussee
import time
start_time = time.time()
with edit(bv2nature):
    ##start an undo block
    bv2nature.beginEditCommand('mise a jour berme')
    for f in bv2nature.getFeatures():
            context.setFeature(f)
            f['surface_nature'] = surUrb.evaluate(context)
            bv2nature.updateFeature(f)
    for f in bv2nature.getFeatures():
            geom = f.geometry()
            f['surface'] = geom.area()
            bv2nature.updateFeature(f)
            context.setFeature(f)
            f['pourc_nature'] = pourUrb.evaluate(context)
            bv2nature.updateFeature(f)
##fin undo block
    bv2nature.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}")  
    
bv1final = bv1nature
bv2final = bv2nature
    
root = QgsProject.instance().layerTreeRoot()
#Find the desired group (which could be a subgroup).
mygroup = root.findGroup("finalisé")  # We assume the group exists
#Load it to the QgsProject (set the second parameter to False since you want to define a custom position for the layer).
QgsProject.instance().addMapLayer(bv1nature, False)
#Add the layer to the desired group.
mygroup.addLayer(bv1nature)#     