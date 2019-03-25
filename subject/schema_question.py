import graphene
from graphene_django import DjangoObjectType
from .models import Question
from .serializers import QuestionSerializer
from general.schema_datapagetype import DataPageType
from general.functions import paginate

class QuestionType(DjangoObjectType):
    class Meta:
        model=Question

class QuestionPageType(DataPageType):
    data=graphene.List(QuestionType)

#query for questions
class Query(graphene.ObjectType):
    question=graphene.Field(QuestionType,id=graphene.Int())
    questions=graphene.Field(QuestionPageType,
        page=graphene.Int(required=True),
        rows=graphene.Int(required=True),
        name=graphene.String(),
    )

    def resolve_question(self,info,**kwargs):
        id=kwargs.get('id')
        if id is not None:
            return Question.objects.get(id=id)

    def resolve_questions(self,info,page,rows,name=None,**kwargs):
        qs=Question.objects.all()


        if name:
            qs=qs.filter(question__icontains=name)
        return paginate(qs,page,rows)

#creating questions
class CreateQuestion(graphene.Mutation):
    question=graphene.Field(QuestionType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        question=graphene.String()
        option1=graphene.String()
        option2=graphene.String()
        option3=graphene.String()
        option4=graphene.String()
        ans=graphene.String()
        chapter=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,**kwargs):
        serializer=QuestionSerializer(data=kwargs)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return CreateQuestion(question=obj,message=msg,status=200)
            

#updating questions
class UpdateQuestion(graphene.Mutation):
    question=graphene.Field(QuestionType)
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.Int(required=True)
        question=graphene.String()
        option1=graphene.String()
        option2=graphene.String()
        option3=graphene.String()
        option4=graphene.String()
        ans=graphene.String()

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        que=Question.objects.get(id=id)
        serializer=QuestionSerializer(que,data=kwargs,partial=True)
        if serializer.is_valid():
            obj=serializer.save()
            msg='success'
        else:
            msg=serializer.errors
            obj=None
            print(msg)
        return UpdateQuestion(question=obj,message=msg,status='200')


#delete Question
class DeleteQuestion(graphene.Mutation):
    status=graphene.String()
    message=graphene.String()

    class Arguments:
        id=graphene.ID(required=True)

    @classmethod
    def mutate(cls,root,info,id,**kwargs):
        que=Question.objects.get(id=id)
        que.delete()
        return DeleteQuestion(message='success',status=200)

class Mutation(graphene.ObjectType):
    create_question=CreateQuestion.Field()
    update_question=UpdateQuestion.Field()
    delete_question=DeleteQuestion.Field()



    
    
