import bpy
import math
import os
from pathlib import Path
import csv




def get_file_path(file_name):
    filepath= bpy.data.filepath
    directory= os.path.dirname(filepath)
    '''Get filepath'''
    file_path = directory+"/"+file_name
    return file_path

def read_csv(file_path):
    '''Read CSV data'''
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def csv_column(data, col):
    '''parse CSV data by index as array'''
    array = []
    for y, row in enumerate(data):
        #ignore the first line (header title)
        if y == 0:
            continue
        array.append(row[col])
    return array


def trigger_update():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
def add_attribute(obj_name, attr_name, type="FLOAT", domain="POINT"):
    attr = bpy.data.objects[obj_name].data.attributes.new(attr_name, type, domain)
    return attr



#********** Read the csv **********
csvfile ="TSNE_TRANSPOSE_3D.csv"

data = read_csv(get_file_path(csvfile))

locx = csv_column(data, 0)
locy = csv_column(data, 1)
locz = csv_column(data, 2)
col = csv_column(data, 3)



#**********Set the object**********

#create the csv collection if it doesn't exist

csvcolexist= False

for colList in bpy.data.collections:
    print(colList.name)
    if colList.name == "csv_imports":
        csvcolexist= True
        break
        
        
if csvcolexist == False:
    csvcol = bpy.data.collections.new("csv_imports")
    bpy.context.scene.collection.children.link(csvcol) #Creates a new collection


#create new mesh data
csvmesh=bpy.data.meshes.new("csvmesh")

#create new object
csvobj = bpy.data.objects.new("csvobject", csvmesh)

#add object to scene
bpy.data.collections['csv_imports'].objects.link(csvobj)

#make the new object active and select it
bpy.context.view_layer.objects.active = csvobj
bpy.context.view_layer.objects.active.select_set(state=True)

#define our active selected object
obj = bpy.context.active_object

#add as many vertices as data lines
obj.data.vertices.add(count = len(locx))

trigger_update()



locx_seq = []

for i in range(len(locx)):
    locx_seq.append(float(locx[i]))

#store the data onto the points
#create a new attribute
attr = add_attribute(obj.name, "locx", 'FLOAT')

#write the csv data into that attribute
attr.data.foreach_set('value', locx_seq)

locy_seq = []

for i in range(len(locx)):
    locy_seq.append(float(locy[i]))

#store the data onto the points
#create a new attribute
attr = add_attribute(obj.name, "locy", 'FLOAT')

#write the csv data into that attribute
attr.data.foreach_set('value', locy_seq)

locz_seq = []

for i in range(len(locz)):
    locz_seq.append(float(locz[i]))

#store the data onto the points
#create a new attribute
attr = add_attribute(obj.name, "locz", 'FLOAT')

#write the csv data into that attribute
attr.data.foreach_set('value', locz_seq)


col_seq = []

for i in range(len(col)):
    col_seq.append(float(col[i]))

#store the data onto the points
#create a new attribute
attr = add_attribute(obj.name, "col", 'FLOAT')

#write the csv data into that attribute
attr.data.foreach_set('value', col_seq)





