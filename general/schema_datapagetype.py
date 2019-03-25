import graphene

class  DataPageType(graphene.ObjectType):
    page=graphene.Int()
    rows=graphene.Int()
    rowCount=graphene.Int()
    pages=graphene.Int()

    def resolve_page(self,info):
        print(self)
        return self['page']

    def resolve_rows(self,info):
        print(self)
        return self['rows']

    def resolve_rowCount(self,info):
        return self['rowCount']

    def resolve_pages(self,info):
        return self['pages']

    def resolve_data(self,info):
        print(self)
        return self['qs']
