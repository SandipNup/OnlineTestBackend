import graphene
from graphene_django import DjangoObjectType
from .models import Topic
from .serializers import TopicSerializer
from general.schema_datapagetype import DataPageType
from general.functions import paginate


class TopicType(DjangoObjectType):
    class Meta:
        model=Topic

class TopicPageType(DataPageType):
    data=graphene.List(TopicType)

class Query(graphene.ObjectType):
    topic=graphene.Field(TopicType,id=graphene.Int(),name=graphene.String())
    topics=graphene.Field(TopicPageType,
        page=graphene.Int(required=True),
        rows=graphene.Int(required=True),
        name=graphene.String(),
        sub_ids=graphene.List(graphene.ID)
    )
    nopaginatetopic=graphene.List(TopicType)


    def resolve_topic(self,info,name=None,**kwargs):
        id=kwargs.get('id')
        if id is not None:
            return Topic.objects.get(id=id)

        if name:
            return Topic.objects.get(name__icontains=name)

    def resolve_topics(self,info,page,rows,name=None,sub_ids=None,**kwargs):
        qs=Topic.objects.all()

        if sub_ids:
            for id in sub_ids:
                qs=qs.filter(subject__id=id)

        if name:
            qs=qs.filter(name__icontains=name)
        return paginate(qs,page,rows)

    def resolve_nopaginatetopic(self,info,**kwargs):
        return Topic.objects.all()

'''Creating Topics'''
class CreateTopic(graphene.Mutation):
    topic=graphene.Field(TopicType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        name=graphene.String(required=True)
        subject = graphene.ID(required=True)


    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer=TopicSerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'

        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return CreateTopic(topic=obj,status=200,message=msg)


'''Updateing topics'''
class UpdateTopic(graphene.Mutation):
    topic=graphene.Field(TopicType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)
        name=graphene.String(required=True)
        subject=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        top=Topic.objects.get(id=id)
        serializer=TopicSerializer(top,data=kwargs,partial=True)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return UpdateTopic(topic=top,message=msg,status=200)


'''deleting topics'''
class DeleteTopic(graphene.Mutation):
    message=graphene.String()
    status=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        top=Topic.objects.get(id=id)
        top.delete()
        return DeleteTopic(status=200,message='success')

class Mutation(graphene.ObjectType):
    create_topic=CreateTopic.Field()
    update_topic=UpdateTopic.Field()
    delete_topic=DeleteTopic.Field()
