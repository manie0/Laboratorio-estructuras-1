from Node import *
from AVLtree import *
import csv
import folium
'''
raiz
print(1730000000.0/1457.0)
print(avl_tree.find(1730000000.0/1457.0))

mas a la derecha
5750000000.0/540.0
'''
avl_tree = AVLTree()

# Insertar datos desde un archivo CSV
avl_tree.insert_csv_data('datos.csv')

#declaracion de mapa
m = folium.Map(location=[20,0], titles ='OpenStreetMap', zoom_start=2)
m2 = folium.Map(location=[20,0], titles ='OpenStreetMap', zoom_start=2)


op1=int(input('1.Seguir - 2.Salir:'))
while(op1 == 1):
    op2 = int(input("1.Generar arbol con dataset \n2.Insertar \n3.Eliminar \n4.Busqueda (metrica) \n 5.Busqueda (Criterio) \n6.Recorrido por niveles"))
    while((op2>=1) and (op2<=6) ):
        
        if op2 == 1:
            #visualizar el arbol en primera instancia con los datos del csv
            avl_tree.visualize_tree()
        elif op2 == 2:
            data = {}  # Crear un diccionario vacío para almacenar los datos

            # Solicitar al usuario que ingrese los valores uno por uno
            data['title'] = input("Ingrese el título: ")
            data['department'] = input("Ingrese el departamento: ")
            data['city'] = input("Ingrese la ciudad: ")
            data['property_type'] = input("Ingrese el tipo de propiedad: ")
            data['latitude'] = float(input("Ingrese la latitud: "))
            data['longitude'] = float(input("Ingrese la longitud: "))
            data['surface_total'] = float(input("Ingrese la superficie total: "))
            data['surface_covered'] = float(input("Ingrese la superficie cubierta: "))
            data['bedrooms'] = int(input("Ingrese la cantidad de dormitorios: "))
            data['bathrooms'] = int(input("Ingrese la cantidad de baños: "))
            data['operation_type'] = input("Ingrese el tipo de operación: ")
            data['price'] = float(input("Ingrese el precio: "))
            avl_tree.insert(data)
            avl_tree.visualize_tree()
        elif op2 == 3:
            #operacion de eliminacion
            price_to_delete = float(input('Ingrese el precio del inmueble a borrar'))
            surface_to_delete = float(input('Ingrese la superficie total del inmueble a borrar'))
            metric_to_delete = price_to_delete/surface_to_delete
            found_data = avl_tree.delete(metric_to_delete)
            #se busca el dato, si no se encuentra es porque efectivamente fue eliminado
            found_data = avl_tree.find(metric_to_delete)
            if found_data:
                print("Dato encontrado (no debería estar):", found_data)
            else:
                print("Dato no encontrado (eliminado)")
            avl_tree.visualize_tree()
        elif op2 == 4:
            # Buscar datos por métrica
            price_to_find = float(input('Ingrese el precio del inmueble a encontrar'))
            surface_to_find = float(input('Ingrese la superficie total del inmueble a encontrar'))
            metric_to_find = price_to_find/surface_to_find
            found_data = avl_tree.find(metric_to_find)
            if found_data:
                print(f"Dato encontrado: {found_data['data']} \nFactor de balanceo: {found_data['balance_factor']} \n Nivel: {found_data['level']} \nPadre:{found_data['parent']} \nAbuelo:{found_data['grandparent']}\nTio: {found_data['uncle']}")
            else:
                print("Dato no encontrado")
            geo = int(input("Geolocalizar?(1.Si)"))
            if geo ==1:
                #guardado de latitudes y longgitudes para visualizacion
                lats = []
                lons = []
                tags = []
                data = found_data['data']
                lat1 = data['latitude']
                lats.append(lat1)
                lon1 = data['longitude']
                lons.append(lon1)
                tags.append("Nodo buscado")
                dataparent = found_data['parent']
                if dataparent is not None:
                    lat2 = dataparent['latitude']
                    lats.append(lat2)
                    lon2 = dataparent['longitude']
                    lons.append(lon2)
                    tags.append("Padre")
                datagrandparent = found_data['grandparent']
                if datagrandparent is not None:
                    lat3 = datagrandparent['latitude']
                    lats.append(lat3)
                    lon3 = datagrandparent['longitude']
                    lons.append(lon3)
                    tags.append("Abuelo")
                
                datauncle = found_data['uncle']
                if datauncle is not None:
                    lat4 = datauncle['latitude']
                    lats.append(lat4)
                    lon4 = datauncle['longitude']
                    lons.append(lon4)
                    tags.append("Tio")
                print(lons)
                print(lats)
                cont = 0
                for lat, lon in zip(lats, lons):
                    folium.Marker([lat, lon], popup = tags[cont] ).add_to(m)
                    cont+=1

                m.save('map.html')
        elif op2 == 5:
            #busqueda por criterios
            criteria = get_criteria()
            matching_nodes = avl_tree.find_matching_nodes(criteria)
            index = 0
            for node in matching_nodes:
                print(f" Indice: {index} data:{node.data} ")
                index+=1
            node_to_find = int(input("Digite el indice del nodo para encontrar: Factor de balanceo, Nivel, Padre, Abuelo y tio"))
            tempnode = matching_nodes[node_to_find]
            tempdict = tempnode.data
                        # Buscar datos por métrica
            price_to_find = tempdict['price']
            surface_to_find = tempdict['surface_total']
            metric_to_find = price_to_find/surface_to_find
            found_data = avl_tree.find(metric_to_find)
            if found_data:
                print(f"Dato encontrado: {found_data['data']} \nFactor de balanceo: {found_data['balance_factor']} \n Nivel: {found_data['level']} \nPadre:{found_data['parent']} \nAbuelo:{found_data['grandparent']}\nTio: {found_data['uncle']}")
            else:
                print("Dato no encontrado")
            geo = int(input("Geolocalizar?(1.Si)"))
            if geo ==1:
                #listas para geolocalizaicon
                lats = []
                lons = []
                tags = []
                data = found_data['data']
                lat1 = data['latitude']
                lats.append(lat1)
                lon1 = data['longitude']
                lons.append(lon1)
                tags.append("Nodo buscado")
                dataparent = found_data['parent']
                if dataparent is not None:
                    lat2 = dataparent['latitude']
                    lats.append(lat2)
                    lon2 = dataparent['longitude']
                    lons.append(lon2)
                    tags.append("Padre")
                datagrandparent = found_data['grandparent']
                if datagrandparent is not None:
                    lat3 = datagrandparent['latitude']
                    lats.append(lat3)
                    lon3 = datagrandparent['longitude']
                    lons.append(lon3)
                    tags.append("Abuelo")
                
                datauncle = found_data['uncle']
                if datauncle is not None:
                    lat4 = datauncle['latitude']
                    lats.append(lat4)
                    lon4 = datauncle['longitude']
                    lons.append(lon4)
                    tags.append("Tio")
                cont=0
                for lat, lon in zip(lats, lons):
                    folium.Marker([lat, lon], popup=tags[cont]).add_to(m2)
                    cont+=1

                m2.save('mapcrit.html')
        
        elif op2 == 6:
            #recorrido por niveles
            result = avl_tree.level_order_traversal()
            print(result)
            
        op1= int(input('1.Seguir - 2.Salir'))
        if op1==1:
            op2 = int(input("1.Generar arbol con dataset \n2.Insertar \n3.Eliminar \n4.Busqueda (metrica) \n 5.Busqueda (Criterio) \n6.Recorrido por niveles"))
        else: 
            op2 = 200000






                
            

        
        

