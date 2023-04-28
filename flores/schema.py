import graphene

import flowers.schema

class Query(flowers.schema.Query, graphene.ObjectType) :
    pass

class Mutation(flowers.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)