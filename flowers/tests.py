from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
import graphene
import json

from flowers.schema import schema
from flowers.models import Flower

FLOWERS_QUERY = '''
    {
    flowers {
        id
        nombreflor
        tipo
        color
        cantidad
        fecha
        ocasion
        precio
        formadepago
        existencias
        direccion
    } 
    }
'''

CREATE_FLOWER_MUTATION = '''
mutation createFlowersMutation($nombreflor: String, $tipo: String, $color: String, $cantidad: Float, $fecha: String, $ocasion: String, $precio: Float, $formadepago: String, $existencias: Float, $direccion: String) {
    createFlower(nombreflor: $nombreflor, tipo: $tipo, color: $color, cantidad: $cantidad, fecha: $fecha, ocasion: $ocasion, precio: $precio, formadepago: $formadepago, existencias: $existencias, direccion: $direccion) {
        nombreflor
    }
}
'''

class FlowersTestCase(GraphQLTestCase) :
    GRAPHQL_SCHEMA = schema
        
    def setUp(self):
        self.flower1 = mixer.blend(Flower)
        
    def test_flowers_query(self):
        response = self.query(
            FLOWERS_QUERY,
            )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        print ("query flowers results")
        print (content)
        assert len(content['data'])==1
        
    def test_createFlower_mutation(self):
        response = self.query(
            CREATE_FLOWER_MUTATION,
            variables={
                'nombreflor': 'Rosalia Uwu',
                'tipo': 'Rosa', 
                'color': 'Rojo', 
                'cantidad': 12.0, 
                'fecha': '2002-04-24', 
                'ocasion': "Nomas", 
                'precio': 5.0, 
                'formadepago': 'Yo', 
                'existencias': 32.0, 
                'direccion': 'En mi casa'}
        )
        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertDictEqual(
            {
                "createFlower": {
                    "nombreflor": "Rosalia Uwu"
                }
            }, 
            content['data']
        )
        
    

# Create your tests here.
