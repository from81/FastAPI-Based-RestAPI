from typing import Dict, List, Optional

from pydantic import BaseModel
from pydantic import Field, validator

from app.model.geometry import BBox, Geometry

# class Position(BaseModel):
#     lat: float
#     lon: float

class Feature(BaseModel):
    """Feature Model"""

    type: str = Field("Feature", const=True)
    geometry: Geometry
    properties: Optional[Dict]
    id: Optional[str]
    bbox: Optional[BBox]

    @validator("geometry", pre=True, always=True)
    def set_geometry(cls, v):
        """set geometry from geo interface or input"""
        # if hasattr(v, "__geo_interface__"):
        #     return v.__geo_interface__
        return v

class FeatureCollection(BaseModel):
    """FeatureCollection Model"""

    type: str = Field("FeatureCollection", const=True)
    features: List[Feature]
    bbox: Optional[BBox]

    def __iter__(self):
        """iterate over features"""
        return iter(self.features)

    def __len__(self):
        """return features length"""
        return len(self.features)

    def __getitem__(self, index):
        """get feature at a given index"""
        return self.features[index]