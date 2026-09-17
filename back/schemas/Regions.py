from pydantic import BaseModel

class Region(BaseModel):
    nom : str
    
class RegionOut(Region):
    id : int