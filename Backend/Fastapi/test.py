from database import session
from model import newsBrands, Base
from typing import List, Dict, Any

def getSentiment(table: List[Dict[str, Any]]):
    content = []
    positive = 0
    negative = 0
    neutral = 0
    for data in table:
        print(data)


data = session.query(newsBrands).filter(newsBrands.name == 'lenovo').all()
getSentiment(data)
# for row in data:
#     print(row)



