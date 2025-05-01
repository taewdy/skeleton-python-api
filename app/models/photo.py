from pydantic import BaseModel


class Photo(BaseModel):
    """Photo model representing a photo from JSONPlaceholder API."""
    album_id: int
    id: int
    title: str
    url: str
    thumbnail_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "album_id": 1,
                "id": 1,
                "title": "accusamus beatae ad facilis cum similique qui sunt",
                "url": "https://via.placeholder.com/600/92c952",
                "thumbnail_url": "https://via.placeholder.com/150/92c952"
            }
        } 