from db.base import endpoints as db

def add(sponsor, sponsor_id, prefix, endpoint):
  db.put(data={"sponsor": sponsor, "sponsor_id": sponsor_id,  "endpoint": endpoint}, key=prefix)
 
def get(prefix):
  item = get(prefix)
  sponsor = item["sponsor"]
  sponsor_id = item["sponsor_id"]
  endpoint = item["endpoint"]
  return sponsor, sponsor_id, endpoint
  
def rm(prefix):
  db.delete(prefix)
  
def get_list():
  items = db.fetch().items
  results = []
  for item in items:
    prefix = item["prefix"]
    sponsor = item["sponsor"]
    result = f"`{prefix}` - **{sponsor}**"
    results.append(result)
  return results