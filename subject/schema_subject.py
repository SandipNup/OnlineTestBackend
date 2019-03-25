import graphene
from graphene_django import DjangoObjectType
from .models import Subject
from .serializers import SubjectSerializer
from . import schema_topic,schema_chapter,schema_question
from general.schema_datapagetype import DataPageType
from general.functions import paginate

class SubjectType(DjangoObjectType):
    image=graphene.String()

    class Meta:
        model=Subject

    
    def resolve_image(self,info):
        return self.image.url
    

class SubjectPageType(DataPageType):
    data=graphene.List(SubjectType)

class Query(schema_topic.Query,schema_chapter.Query,schema_question.Query,graphene.ObjectType):
    subject=graphene.Field(SubjectType,id=graphene.Int(),name=graphene.String())
    subjects=graphene.Field(SubjectPageType,
        page=graphene.Int(required=True),
        rows=graphene.Int(required=True),
        name=graphene.String(),
    )
    nopaginatesub=graphene.List(SubjectType)

    def resolve_subject(self,info,name=None,**kwargs):
        id=kwargs.get('id')
        if id is not None:
            return Subject.objects.get(pk=id)

        if name:
            return Subject.objects.get(name__icontains=name)

    def resolve_subjects(self,info,page,rows,name=None,**kwargs):
        qs=Subject.objects.all()
        print(name)

        if name:
            qs=qs.filter(name__icontains=name)
        return paginate(qs,page,rows)

    def resolve_nopaginatesub(self,info,**kwargs):
        return Subject.objects.all()

    

#creating subject
class CreateSubject(graphene.Mutation):
    subject=graphene.Field(SubjectType)
    message=graphene.String()
    status=graphene.String()

    class Arguments:
        name=graphene.String(required=True)
        image=graphene.String(required=True)
        description=graphene.String(required=True)
   
    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer=SubjectSerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return CreateSubject(subject=obj,message=msg,status=200)


'''Updating subject'''
class UpdateSubject(graphene.Mutation):
    subject=graphene.Field(SubjectType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)
        name=graphene.String()
        image=graphene.String()
        description=graphene.String()

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        sub=Subject.objects.get(id=id)
        serializer=SubjectSerializer(sub,data=kwargs,partial=True)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return UpdateSubject(subject=obj,message=msg,status=200)


'''Delete Subject'''
class DeleteSubject(graphene.Mutation):
    message=graphene.String()
    status=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        c=Subject.objects.get(id=id)
        c.delete()
        return DeleteSubject(message='success',status=200)


class Mutation(schema_topic.Mutation,schema_chapter.Mutation,schema_question.Mutation,graphene.ObjectType):
    create_subject=CreateSubject.Field()
    update_subject=UpdateSubject.Field()
    delete_subject=DeleteSubject.Field()


    