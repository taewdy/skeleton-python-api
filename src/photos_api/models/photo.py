from pydantic import BaseModel, Field


class Photo(BaseModel):
    """Photo model representing a photo from the external API."""
    
    album_id: int = Field(..., alias="albumId", description="Album ID that the photo belongs to")
    id: int = Field(..., description="Unique identifier for the photo")
    title: str = Field(..., description="Title of the photo")
    url: str = Field(..., description="URL of the full-size photo")
    thumbnail_url: str = Field(..., alias="thumbnailUrl", description="URL of the thumbnail photo")
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "albumId": 1,
                "id": 1,
                "title": "accusamus beatae ad facilis cum similique qui sunt",
                "url": "https://via.placeholder.com/600/92c952",
                "thumbnailUrl": "https://via.placeholder.com/150/92c952"
            }
        }