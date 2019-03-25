import graphene
import subject.schema_subject
import users.schema
import graphql_jwt



class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(users.schema.UserType)

    @classmethod
    def resolve(cls, root, info):
        return cls(user=info.context.user)

class Query(users.schema.Query,subject.schema_subject.Query,graphene.ObjectType):
    pass

class Mutation(users.schema.Mutation,
    subject.schema_subject.Mutation,
    graphene.ObjectType):


    token_auth = ObtainJSONWebToken.Field()

    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass

schema=graphene.Schema(query=Query,mutation=Mutation)