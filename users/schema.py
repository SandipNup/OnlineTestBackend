from django.contrib.auth import get_user_model
import graphene 
from graphene_django import DjangoObjectType
from .serializers import UserSerializer
from general.schema_datapagetype import DataPageType
from general.functions import paginate


class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()

class UserPageType(DataPageType):
    data=graphene.List(UserType)

'''Query for users'''
class Query(graphene.ObjectType):
    me=graphene.Field(UserType,id=graphene.Int())
    users=graphene.Field(UserPageType,
        page=graphene.Int(required=True),
        rows=graphene.Int(required=True),
        name=graphene.String(),
    )

    def resolve_me(self,info,**kwargs):
        user=info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged !')
        return user

    def resolve_users(self,info,page,rows,name=None,module=None,**kwargs):
        qs=get_user_model().objects.all()

        if name:
            qs=qs.filter(username__icontains=name)
        return paginate(qs,page,rows)

'''Creating users'''
class CreateUser(graphene.Mutation):
    user=graphene.Field(UserType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        username=graphene.String(required=True)
        email=graphene.String(required=True)
        password=graphene.String()
        name = graphene.String(required=True)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer=UserSerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)

        return CreateUser(user=obj,message=msg,status=200)


#updating user
class UpdateUser(graphene.Mutation):
    user=graphene.Field(UserType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)
        username=graphene.String()
        email=graphene.String()
        password=graphene.String()
        name = graphene.String()

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        user=get_user_model().objects.get(id=id)
        serializer=UserSerializer(user,data=kwargs,partial=True)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return UpdateUser(user=obj,message=msg,status=200)


#deleting user
class DeleteUser(graphene.Mutation):
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        user=get_user_model().objects.get(id=id)
        user.delete()
        return DeleteUser(status=200,message='success')


class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()
    update_user=UpdateUser.Field()
    delete_user=DeleteUser.Field()
