import math

def paginate(p,page,rows):
    rowCount=p.count()

    pages=math.ceil(rowCount/rows)

    if page>pages:
            page=1
            offset=0

    else:
        offset=(page-1)*rows

    qs=p[offset::][:rows]
    return {'qs':qs,'page':page,'rows':rows,'rowCount':rowCount,'pages':pages}