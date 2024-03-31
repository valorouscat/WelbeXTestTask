from pydantic import BaseModel, field_validator
from typing import List

class Coordinate(BaseModel):
    lat: float = None
    lng: float = None

    class Config:
        extra = 'allow'

class PointBase(BaseModel):
    points: List[Coordinate] = None

    @field_validator('points', mode='before')
    def validate_points(cls, v):
        # Validate that each point is a dictionary with 'lat' and 'lng' keys
        for point in v:
            if not isinstance(point, dict) or 'lat' not in point or 'lng' not in point:
                raise ValueError('Each point must be a dictionary with keys "lat" and "lng"')
        return v
