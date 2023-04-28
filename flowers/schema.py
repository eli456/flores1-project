import graphene
from graphene_django import DjangoObjectType

from .models import Flower

class FlowerType(DjangoObjectType) :
    class Meta :
        model = Flower

class Query(graphene.ObjectType) : 
    flowers = graphene.List(FlowerType)
    
    def resolve_flowers(self, info, **kwargs) :
        return Flower.objects.all()

class CreateFlowers(graphene.Mutation) :
    id = graphene.Int()
    nombreflor = graphene.String()
    tipo = graphene.String()
    color = graphene.String()
    cantidad = graphene.Float()
    fecha = graphene.String()
    ocasion = graphene.String()
    precio = graphene.Float()
    formadepago = graphene.String()
    existencias = graphene.Float()
    direccion = graphene.String()
    
    class Arguments :
        nombreflor = graphene.String()
        tipo = graphene.String()
        color = graphene.String()
        cantidad = graphene.Float()
        fecha = graphene.String()
        ocasion = graphene.String()
        precio = graphene.Float()
        formadepago = graphene.String()
        existencias = graphene.Float()
        direccion = graphene.String()
        
    def mutate(self, info,  nombreflor, tipo, color, cantidad, fecha, ocasion, precio, formadepago, existencias, direccion ) :
        flor = Flower( nombreflor = nombreflor, tipo = tipo, color = color, cantidad = cantidad, fecha = fecha, ocasion = ocasion, precio = precio, formadepago = formadepago, existencias = existencias, direccion = direccion)
        flor.save()
        
        return CreateFlowers(
            id = flor.id, 
            nombreflor = flor.nombreflor,
            tipo = flor.tipo,
            color = flor.color,
            cantidad = flor.cantidad,
            fecha = flor.fecha,
            ocasion = flor.ocasion,
            precio = flor.precio,
            formadepago = flor.formadepago,
            existencias = flor.existencias,
            direccion = flor.direccion
        )
        
class Mutation(graphene.ObjectType) :
    create_flower = CreateFlowers.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
        