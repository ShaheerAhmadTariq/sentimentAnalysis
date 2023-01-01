from database import session
from model import newsBrands,newsCompetitor,newsHashtag

def getNewsBrand():
    results = session.query(newsBrands).all()
    name = 'vivo'
    return session.query(newsBrands).filter(newsBrands.name == name).all()
# # Iterate through the list and print out the data for each record
#     for record in results:
#         print(record.source_id, record.source_name, record.author, record.title, record.description, record.url, record.url_to_image, record.published_at, record.content, record.name)