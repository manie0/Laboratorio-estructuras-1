import csv
from Node import *
import pydotplus
from graphviz import Digraph
import folium

class AVLTree:
    def __init__(self):
        self.root = None

    def find_matching_nodes(self, criteria):
            return self._find_matching_nodes(self.root, criteria)

    def _find_matching_nodes(self, node, criteria):
        if node is None:
            return []
        matching_nodes = []
        if node.matches_criteria(criteria):
            matching_nodes.append(node)
        matching_nodes.extend(self._find_matching_nodes(node.left, criteria))
        matching_nodes.extend(self._find_matching_nodes(node.right, criteria))
        return matching_nodes

    def height(self, node):
        if node is None:
            return 0
        return node.height



    def balance_factor(self, node):
        if node is None:
            return 0
        #se utiliza altura izquierda menos derecha, todo el arbol esta programado para trabajar con este balanceo
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def rotate_left(self, node):
        right_child = node.right
        if right_child is None:
            return node  # No es posible realizar la rotación
        node.right = right_child.left
        right_child.left = node
        self.update_height(node)
        self.update_height(right_child)
        return right_child

    def rotate_right(self, node):
        left_child = node.left
        if left_child is None:
            return node  # No es posible realizar la rotación
        node.left = left_child.right
        left_child.right = node
        self.update_height(node)
        self.update_height(left_child)
        return left_child

    def insert(self, data):
        """
        Inserta un nodo con datos en el árbol AVL.

        Args:
            data (dict): Los datos a insertar en el árbol.
        """
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        """
        Función auxiliar para insertar un nodo con datos en el árbol AVL.

        Args:
            node (Node): El nodo actual en el proceso de inserción.
            data (dict): Los datos a insertar en el árbol.

        Returns:
            Node: El nuevo nodo raíz después de la inserción.
        """
        if node is None:
            return Node(data)

        primary_metric = data['price'] / data['surface_total']
        node_metric = node.data['price'] / node.data['surface_total']

        if primary_metric < node_metric:
            node.left = self._insert(node.left, data)
        elif primary_metric > node_metric:
            node.right = self._insert(node.right, data)
        else:
            #caso valores repetidos
            primary_secondary_metric = (data['bedrooms'] * 0.4) + (data['bathrooms'] * 0.3) + (data['surface_total'] * 0.2) + (data['surface_covered'] * 0.1)
            node_secondary_metric = (node.data['bedrooms'] * 0.4) + (node.data['bathrooms'] * 0.3) + (node.data['surface_total'] * 0.2) + (node.data['surface_covered'] * 0.1)

            if primary_secondary_metric <= node_secondary_metric:
                node.left = self._insert(node.left, data)
            else:
                node.right = self._insert(node.right, data)

        self.update_height(node)
        #balanceo
        balance = self.balance_factor(node)

        if balance > 1:
            if primary_metric < node.left.data['price'] / node.left.data['surface_total']:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if primary_metric > node.right.data['price'] / node.right.data['surface_total']:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def find(self, metric):
        """
        Busca un nodo en el árbol AVL por su métrica primaria.

        Args:
            metric (float): La métrica primaria para buscar.

        Returns:
            dict: Los datos del nodo encontrado o None si no se encuentra.
        """
        return self._find(self.root, metric)

    # Función para encontrar un nodo y obtener información adicional
    def find(self, metric):
        return self._find(self.root, metric)

    def _find(self, node, metric, level=1, parent=None, grandparent=None):
        if node is None:
            return None

        primary_metric = node.data['price'] / node.data['surface_total']
         # Se ha encontrado el nodo deseado, devuelve un diccionario con la información solicitada
        if metric == primary_metric:
            return {
                'data': node.data,
                'level': level,
                'balance_factor': self.balance_factor(node),
                'parent': parent.data if parent else None,
                'grandparent': grandparent.data if grandparent else None,
                'uncle': grandparent.left.data if grandparent and grandparent.left != parent else grandparent.right.data if grandparent and grandparent.right != parent else None
            }

        if metric < primary_metric:
             # Busca en el subárbol izquierdo
            return self._find(node.left, metric, level + 1, parent=node, grandparent=parent)
        else:
             # Busca en el subárbol derecho
            return self._find(node.right, metric, level + 1, parent=node, grandparent=parent)


    def delete(self, metric):
        """
        Elimina un nodo en el árbol AVL por su métrica primaria.

        Args:
            metric (float): La métrica primaria para eliminar.
        """
        self.root = self._delete(self.root, metric)

    def _delete(self, node, metric):
        """
        Función auxiliar para eliminar un nodo en el árbol AVL por su métrica primaria.

        Args:
            node (Node): El nodo actual en el proceso de eliminación.
            metric (float): La métrica primaria para eliminar.

        Returns:
            Node: El nuevo nodo raíz después de la eliminación.
        """
        if node is None:
            return node

        if metric < node.data['price'] / node.data['surface_total']:
            node.left = self._delete(node.left, metric)
        elif metric > node.data['price'] / node.data['surface_total']:
            node.right = self._delete(node.right, metric)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            min_node = self._find_min(node.right)
            node.data = min_node.data
            node.right = self._delete(node.right, min_node.data['price'] / min_node.data['surface_total'])

        self.update_height(node)
        #balanceo
        balance = self.balance_factor(node)

        if balance > 1:
            if self.balance_factor(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.balance_factor(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def find_min(self):
        """
        Encuentra el nodo con la métrica primaria más baja en el árbol.

        Returns:
            dict: Los datos del nodo con la métrica primaria más baja.
        """
        min_node = self._find_min(self.root)
        if min_node:
            return min_node.data
        else:
            return None

    def _find_min(self, node):
        """
        Función auxiliar para encontrar el nodo con la métrica primaria más baja en el árbol.

        Args:
            node (Node): El nodo actual en el proceso de búsqueda.

        Returns:
            Node: El nodo con la métrica primaria más baja.
        """
        if node is None or node.left is None:
            return node
        return self._find_min(node.left)

    def level_order_traversal(self):
        """
        Realiza un recorrido por niveles del árbol AVL utilizando una función recursiva.

        Returns:
            list: Una lista con los datos de los nodos en orden de recorrido por niveles.
        """
        result = []

        def traverse(node, depth):
            if node is not None:
                if len(result) <= depth:
                    result.append([])
                result[depth].append(node.data['title'])
                traverse(node.left, depth + 1)
                traverse(node.right, depth + 1)

        traverse(self.root, 0)
        #retorna una lista de listas, dentro de cada lista se contiene los nodos de un nivel
        return [data for sublist in result for data in sublist]

    def insert_csv_data(self, csv_file):
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data = {
                'title': row['title'],
                'department': row['department'],
                'city': row['city'],
                'property_type': row['property_type'],
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude']),
                'surface_total': float(row['surface_total']),
                'surface_covered': float(row['surface_covered']),
                'bedrooms': float(row['bedrooms']),
                'bathrooms': float(row['bathrooms']),
                'operation_type': row['operation_type'],
                'price': float(row['price'])
                }
                self.insert(data)

    def visualize_tree(self):
        """
        Visualiza el árbol AVL utilizando Graphviz, mostrando 'title', 'department', 'city', la primera métrica y el factor de balanceo.
        """
        dot = Digraph(format='png', engine='dot')
        dot.attr(dpi='65')

        def add_nodes(node):
            if node is not None:
                # Crear una etiqueta personalizada con 'title', 'department', 'city', la primera métrica y el factor de balanceo
                label = f"Title: {node.data['title']}\\nDepartment: {node.data['department']}\\nCity: {node.data['city']}\\nPrimary Metric: {node.data['price'] / node.data['surface_total']}\\nBalance Factor: {self.balance_factor(node)}"
                unique_label = str(id(node))  # Generar una etiqueta única para cada nodo
                dot.node(unique_label, label)
                if node.left:
                    left_unique_label = str(id(node.left))
                    dot.edge(unique_label, left_unique_label)
                    add_nodes(node.left)
                if node.right:
                    right_unique_label = str(id(node.right))
                    dot.edge(unique_label, right_unique_label)
                    add_nodes(node.right)

        if self.root:
            add_nodes(self.root)

        dot.render('avl_tree')  # Genera el archivo "avl_tree.png" en el directorio actual

    def get_balance_factors(self):
        """
        Obtiene y muestra los factores de balance para cada nodo en el árbol AVL., se uso para testear que no haya ningun factor de balanceo erroneo
        """
        def calculate_balance_factors(node):
            if node is not None:
                balance = self.balance_factor(node)
                print(f"Node: {node.data}, Balance Factor: {balance}")
                calculate_balance_factors(node.left)
                calculate_balance_factors(node.right)

        if self.root:
            print("Balance Factors:")
            calculate_balance_factors(self.root)

def get_criteria():
    fields = [
        'title', 'department', 'city', 'property_type', 'latitude', 'longitude',
        'surface_total', 'surface_covered', 'bedrooms', 'bathrooms', 'operation_type', 'price'
    ]
    operators = {
        '1': '=',
        '2': '<',
        '3': '>',
        '4': '<=',
        '5': '>='
    }
    criteria = {}
    print("Ingrese hasta 3 criterios de búsqueda:")
    for i in range(3):
        field = input(f"Campo de búsqueda {i+1} (Elija uno de: {', '.join(fields)}): ")
        if field not in fields:
            print(f"Campo no válido: {field}. Por favor, elija uno de los siguientes: {', '.join(fields)}")
            continue
        operator = input(f"Operador para {field} (1: '=', 2: '<', 3: '>', 4: '<=', 5: '>='): ")
        if operator not in operators:
            print(f"Operador no válido: {operator}. Por favor, elija uno de los siguientes: 1: '=', 2: '<', 3: '>', 4: '<=', 5: '>='")
            continue
        value = input(f"Valor para {field}: ")
        if field in ['latitude', 'longitude', 'surface_total', 'surface_covered', 'bedrooms', 'bathrooms', 'price']:
            try:
                value = float(value)
            except ValueError:
                print(f"Valor no válido: {value}. Por favor, ingrese un número.")
                continue
        criteria[field] = (operators[operator], value)
    return criteria



