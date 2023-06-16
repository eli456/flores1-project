import graphene
from graphene_django import DjangoObjectType
from .models import Flower
from graphql import GraphQLError
from django.db.models import Q
from users.schema import UserType
from flowers.models import Flower, Vote

class FlowerType(DjangoObjectType) :
    class Meta :
        model = Flower
        
class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType) : 
    flowers = graphene.List(FlowerType, search=graphene.String())
    votes = graphene.List(VoteType)
    
    def resolve_flowers(self, info, search=None, **kwargs) :
        if search:
            filter = (
                Q(nombreflor__icontains=search) |
                Q(tipo__icontains=search)
            )
            return Flower.objects.filter(filter)
        return Flower.objects.all()
    
    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

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
    posted_by = graphene.Field(UserType)

    
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
        
        user = info.context.user or None
        
        flor = Flower( nombreflor = nombreflor, tipo = tipo, color = color, cantidad = cantidad, fecha = fecha, ocasion = ocasion, precio = precio, formadepago = formadepago, existencias = existencias, direccion = direccion, posted_by=user,)
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
            direccion = flor.direccion,
            posted_by=flor.posted_by
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    flor = graphene.Field(FlowerType)

    class Arguments:
        flor_id = graphene.Int()

    def mutate(self, info, flor_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to vote!')

        flower = Flower.objects.filter(id=flor_id).first()
        if not flower:
            raise GraphQLError('Invalid Dlor!')

        Vote.objects.create(
            user=user,
            flower=flower,
        )

        return CreateVote(user=user, flower=flower)

class Mutation(graphene.ObjectType) :
    create_flower = CreateFlowers.Field()
    create_link = CreateFlowers.Field()
    create_vote = CreateVote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)