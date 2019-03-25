import graphene
from graphene_django import DjangoObjectType
from .models import Chapter
from .serializers import ChapterSerializer
from general.schema_datapagetype import DataPageType
from general.functions import paginate


class ChapterType(DjangoObjectType):
    class Meta:
        model=Chapter

class ChapterPageType(DataPageType):
    data=graphene.List(ChapterType)


#query for chapter
class Query(graphene.ObjectType):
    chapter=graphene.Field(ChapterType,id=graphene.Int())
    chapters=graphene.Field(ChapterPageType,
        page=graphene.Int(required=True),
        rows=graphene.Int(required=True),
        name=graphene.String(),
        sub_ids=graphene.List(graphene.ID),
        topic_ids=graphene.List(graphene.ID)
    )

    def resolve_chapter(self,info,**kwargs):
        id=kwargs.get('id')
        if id is not None:
            return Chapter.objects.get(id=id)

    def resolve_chapters(self,info,page,rows,name=None,sub_ids=None,topic_ids=None,**kwargs):
        qs=Chapter.objects.all()

        if name:
            qs=qs.filter(name__icontains=name)

        if sub_ids:
            for id in sub_ids:
                qs=qs.filter(topic__subject__id=id)

        if topic_ids:
            for id in topic__ids:
                qs=qs.filter(topic__id=id)

        return paginate(qs,page,rows)

#creating chapter
class CreateChapter(graphene.Mutation):
    chapter=graphene.Field(ChapterType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        name=graphene.String()
        basic_theory=graphene.String()
        topic=graphene.ID(required=True)
        subject=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer=ChapterSerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return CreateChapter(chapter=obj,message=msg,status=200)

#updating chapter
class UpdateChapter(graphene.Mutation):
    chapter=graphene.Field(ChapterType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)
        name=graphene.String()
        basic_theory=graphene.String()
        topic=graphene.ID(required=True)
        subject=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        chap=Chapter.objects.get(id=id)
        serializer=ChapterSerializer(chap,data=kwargs,partial=True)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return UpdateChapter(chapter=obj,message=msg,status=200)

#delete chapter
class DeleteChapter(graphene.Mutation):
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        chap=Chapter.objects.get(id=id)
        chap.delete()
        return DeleteChapter(status=200,message='success')

class Mutation(graphene.ObjectType):
    create_chapter=CreateChapter.Field()
    update_chapter=UpdateChapter.Field()
    delete_chapter=DeleteChapter.Field()