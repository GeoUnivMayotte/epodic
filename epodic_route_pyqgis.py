#nom des couches dans le projet
project =  QgsProject.instance()
print(project.mapLayers())
for id, layer in project.mapLayers().items():
        print(layer.name())
#sélection variables routes & bassin versant
route = QgsProject.instance().mapLayersByName('troncon_de_route')[0]
bv1=QgsProject.instance().mapLayersByName('bassin_versant_topographique')[0]
bv2=QgsProject.instance().mapLayersByName('l_bassin_versant_s_976')[0]

##processus de calcul pour remplacer null par 0
import time
start_time = time.time()
with edit(route):
        ##start an undo block
    route.beginEditCommand('transformation null en 0')
    for f in route.getFeatures():
        attributes = f.attributes()
        new_attributes = [a or 0 for a in attributes]
        f.setAttributes(new_attributes)
        route.updateFeature(f)
        ##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

# définition nouveaux champ pour la couche route
fieldlcorr = QgsField("l_corrigee", QVariant.Double)
fieldlbdd = QgsField("l_bande_derasee", QVariant.Double)
fieldlberme = QgsField("l_berme", QVariant.Double)
fieldlchaussee = QgsField("l_chaussee", QVariant.Double)
fieldlemprise = QgsField("l_emprise", QVariant.Double)
fieldLemprise = QgsField("Long_ligne", QVariant.Double)

#ajout nouveaux champs dans la couche route
route.dataProvider().addAttributes([fieldlcorr, fieldlbdd, fieldlberme,fieldlchaussee, fieldlemprise, fieldLemprise])
route.updateFields()
print ([f.name() for f in route.fields()])

##mise à jour champ grace a un autre champ 
# définition variables
type_route = 'cpx_classement_administratif'
nature_route = 'nature'
surface = 'surface_emprise'
berme = 'l_berme'
corrigee = 'l_corrigee'
der = 'l_bande_derasee'


# print(iface.activeLayer().name())
# print(iface.activeLayer().featureCount())

##autre essai pour ajouter infos en fonction autre champ l corrigee

##mise à jour l_corrigée
import time
start_time = time.time()
with edit(route):
    ##start an undo block
    route.beginEditCommand('mise a jour berme')
    # request = QgsFeatureRequest()
    for feature in route.getFeatures():
            if feature[type_route] == "Nationale":
                feature[corrigee] = 3.5
            elif feature['cpx_classement_administratif'] ==  "Départementale" and  feature['nature']  ==  "Route à 1 chaussée": 
                feature['l_corrigee']= 3
            elif feature['nature']  ==  "Route à 2 chaussées":
                feature['l_corrigee']= 3.5
            elif feature['nature'] in ("Chemin", "Escalier" , "Piste cyclable" , "Route empierrée" , "Sentier" , "Rond-point" ,  "Route à 1 chaussée"):
                feature['l_corrigee']= 2
            else:
                feature[corrigee]= 2.5
            route.updateFeature(feature)
##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"The execution time is: {end_time-start_time}")


##mise à jour berme 
import time
start_time = time.time()
with edit(route):
    ##start an undo block
    route.beginEditCommand('mise a jour berme')
    request = QgsFeatureRequest()
 ##   request.setFlags(QgsFeatureRequest.NoGeometry)
##    request.setSubsetOfAttributes([0,2])
    for feature in route.getFeatures(request):
        if feature['nature'] in ("Chemin" , "Escalier" , "Piste cyclable" , "Route empierrée" , "Sentier"):
            feature[berme]=0
        else:
            feature[berme]=1
        route.updateFeature(feature)
        ##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}")
       
        
##mise à jour bande dérasée
import time
start_time = time.time()
with edit(route):
    ##start an undo block
    route.beginEditCommand('mise a jour berme')
    for feature in route.getFeatures():
        if feature['nature'] in ("Chemin" , "Escalier" , "Piste cyclable" , "Route empierrée" , "Sentier"):
            feature[der] = 0
        elif feature['nature'] == "Rond-point":
            feature[der] = 0.5
        elif feature['nature']=='Route à 1 chaussée' and  feature["nombre_de_voies"]  <=  1: 
            feature[der]=0.5
        elif feature['nature']=='Route à 1 chaussée' and  feature["nombre_de_voies"]  >=  2:
            feature[der]=1
        elif feature['nature']=='Route à 2 chaussées' and  feature["nombre_de_voies"]  <= 1:
            feature[der]=1.5
        elif feature['nature']=='Route à 2 chaussées' and  feature["nombre_de_voies"]   >= 2:
            feature[der]=2.5
        route.updateFeature(feature)    
        ##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}")  
    


##mise a jour champ l chaussee grace a un autre champ (essai avec commandes anita graser)
lchaussee = QgsExpression('nombre_de_voies * l_corrigee')
##To execute our expressions, we need to provide an appropriate QgsExpressionContext. To set it up, use:
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(route)
##largeur chaussee
#import time
start_time = time.time()
with edit(route):
    ##start an undo block
    route.beginEditCommand('mise a jour berme')
    for feature in route.getFeatures():
        if feature['nombre_de_voies'] == 0:
            feature['l_chaussee'] = 2
        else:
            context.setFeature(feature)
            feature['l_chaussee'] = lchaussee.evaluate(context)
        route.updateFeature(feature)
##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution chaussée : {end_time-start_time}") 

##mise à jour champ 
lemprise = QgsExpression('l_bande_derasee + l_berme + l_chaussee')
##To execute our expressions, we need to provide an appropriate QgsExpressionContext. To set it up, use:
context = QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(r))
## lancer commandes mise à jour
with edit(r):
        ##start an undo block
    route.beginEditCommand('mise a jour berme')
    for f in route.getFeatures():
        context.setFeature(f)
        f['l_emprise'] = lemprise.evaluate(context)
        route.updateFeature(f)
##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution emprise : {end_time-start_time}") 
    
##création buffer de la taille emprise qui permettra ensuite de calculer l'aire de la route'    
tampon = processing.run("native:buffer", {'INPUT':route,
'DISTANCE':QgsProperty.fromExpression('"l_emprise" /2'), ##on peut aussi utiliser expression pour plus facile
'SEGMENTS':5,
'END_CAP_STYLE':0,
'JOIN_STYLE':0,
'MITER_LIMIT':2,
'DISSOLVE':False,'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']  

##ajout champ aire emprise à partir tampon créé
fieldaemprise = QgsField("surface_emprise", QVariant.Double)
##ajout champ surface emprise
tampon.dataProvider().addAttributes([fieldaemprise])
tampon.updateFields()
print ([f.name() for f in tampon.fields()])
with edit(tampon):
        ##start an undo block
    route.beginEditCommand('calcul géométrie tampon emprise')
    for f in tampon.getFeatures():
        geom = f.geometry()
        f['surface_emprise'] = geom.area()
        tampon.updateFeature(f)
##fin undo block
    route.endEditCommand()
    end_time = time.time()
    print(f"Temps d\'execution : {end_time-start_time}") 

#intersection entre tampon et chaque bv    
import time
start_time = time.time()
        ##start an undo block
route.beginEditCommand('')    
bvTotalIntersection = processing.runAndLoadResults("native:intersection", {'INPUT':tampon,
    'OVERLAY':bvTotal,
    'INPUT_FIELDS':['cleabs','nature','l_emprise'],
    'OVERLAY_FIELDS':['cleabs'],
    'OVERLAY_FIELDS_PREFIX':'bv1_',
    'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']
##fin undo block
route.endEditCommand()
end_time = time.time()
print(f"Temps d\'execution : {end_time-start_time}")

    
QgsProject.instance().addMapLayer(buffered_bv1)
QgsProject.instance().addMapLayer(buffered_bv2)
 
