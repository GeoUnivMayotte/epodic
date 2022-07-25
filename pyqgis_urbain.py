# Get input (csv) and target (Shapefile) layers
# bv1=QgsProject.instance().mapLayersByName('bv_epodic bv_type1_unique_station_epodic')[0]
# bv2=QgsProject.instance().mapLayersByName('bv_epodic bv_type2_unique_station_epodic')[0]
bvTotal=QgsProject.instance().mapLayersByName('bassin_versant_topographique')[0]
sport=QgsProject.instance().mapLayersByName('terrain_sport_urbain_surface_bvtype2')[0]
route =QgsProject.instance().mapLayersByName('route-surface_bvtype2_total')[0] # <- vérifié concordance jeu de donnée
batsurf=QgsProject.instance().mapLayersByName('batiment_surface_bvtype2')[0]
batnomb=QgsProject.instance().mapLayersByName('batiment-nombre_bvtype2')[0]

# Set properties for the join
bv1Field='cleabs'
bv2Field = 'id_obj'
sport1='cleabs_2'
route1='bv1_cleabs'
batsur1='cleabs'
batnomb1='cleabs'
sport2='id_obj'
route2='id_obj'
batsurf2='id_obj'
batnomb2='id_obj'

s = processing.run("native:joinattributestable", {
'INPUT':bv2,
'FIELD':bv2Field,
'INPUT_2':sport,
'FIELD_2':sport2,
'FIELDS_TO_COPY':['None'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'sport_surf_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

r = processing.run("native:joinattributestable", {
'INPUT':s,
'FIELD':bv2Field,
'INPUT_2':route,
'FIELD_2':route2,
'FIELDS_TO_COPY':['None'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'route_surf_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

bs = processing.run("native:joinattributestable", {
'INPUT':r,
'FIELD':bv2Field,
'INPUT_2':batsurf,
'FIELD_2':batsurf2,
'FIELDS_TO_COPY':['None'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'bat_surf_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

bn = processing.run("native:joinattributestable", {
'INPUT':bs,
'FIELD':bv2Field,
'INPUT_2':batnomb,
'FIELD_2':batnomb2,
'FIELDS_TO_COPY':['None'],
'METHOD':0,
'DISCARD_NONMATCHING':False,
'PREFIX':'bat_nomb_',
'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

#suppression champ
idField =bn.dataProvider().fieldNameIndex("pourc_urbain")
p = bn.dataProvider().fieldNameIndex("urbain_surface_bvtype2_None")
bn.dataProvider().deleteAttributes([idField, p])
bn.updateFields()

#changement nom champ
#à lancer l'une après l'autre''
for field in bn.fields():
    if field.name() == 'sport_surf_None':
        with edit(bn):
            idx = bn.fields().indexFromName(field.name())
            bn.renameAttribute(idx, 'sport_surface')
for field in bn.fields():
    if field.name() == 'route_surf_None':
        with edit(bn):            
            idx = bn.fields().indexFromName(field.name())
            bn.renameAttribute(idx, 'route_surface')
for field in bn.fields():
    if field.name() == 'bat_surf_None':
        with edit(bn):            
            idx = bn.fields().indexFromName(field.name())
            bn.renameAttribute(idx, 'bat_surface')
for field in bn.fields():
    if field.name() == 'bat_nomb_None':
        with edit(bn):            
            idx = bn.fields().indexFromName(field.name())
            bn.renameAttribute(idx, 'bat_nombre')

# ajout nouveau champ (somme surface bat terrain et route)
# définition du champ à créer
surface = QgsField("surface", QVariant.Double)
sururb = QgsField("surface_urbain", QVariant.Double)
poururb = QgsField("pourc_urbain", QVariant.Double)

##ajout champ
bn.dataProvider().addAttributes([surface, sururb,poururb])

#mise à jour des champs dans la couche
bn.updateFields()

##remplacer null par 0
import time
start_time = time.time()
with edit(bn):
        ##start an undo block
    bn.beginEditCommand('mise a jour berme')
    for f in bn.getFeatures():
        attributes = f.attributes()
        new_attributes = [a or 0 for a in attributes]
        f.setAttributes(new_attributes)
        bn.updateFeature(f)
        ##fin undo block
    bn.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

# calcul surface urbain
surUrb = QgsExpression('sport_surface + route_surface + bat_surface')
pourUrb = QgsExpression('surface_urbain/ surface * 100')
#expression à calculer et définition variable
##To execute our expressions, we need to provide an appropriate QgsExpressionContext. To set it up, use:
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(bn)
##largeur chaussee
import time
start_time = time.time()
with edit(bn):
    ##start an undo block
    bn.beginEditCommand('mise a jour berme')
    for f in bn.getFeatures():
            context.setFeature(f)
            f['surface_urbain'] = surUrb.evaluate(context)
            bn.updateFeature(f)
    for f in bn.getFeatures():
            geom = f.geometry()
            f['surface'] = geom.area()
            bn.updateFeature(f)
            context.setFeature(f)
            f['pourc_urbain'] = pourUrb.evaluate(context)
            bn.updateFeature(f)
##fin undo block
    bn.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

#Get the reference of the layer tree.

root = QgsProject.instance().layerTreeRoot()
#Find the desired group (which could be a subgroup).
mygroup = root.findGroup("finalisé")  # We assume the group exists
#Load it to the QgsProject (set the second parameter to False since you want to define a custom position for the layer).
QgsProject.instance().addMapLayer(bn, False)
#Add the layer to the desired group.
mygroup.addLayer(bn)# 

iface.showAttributeTable(bn)

#project.mapLayersByName('Intersection')[0].setName("metro_1000m") <- renommer couche dans le projet (nom ancien -> nom nouveau)