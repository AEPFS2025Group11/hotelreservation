from pydantic import BaseModel


class FacilityIn(BaseModel):
    facility_name: str

    model_config = {'from_attributes': True}


class FacilityOut(BaseModel):
    facility_id: int
    facility_name: str

    model_config = {'from_attributes': True}


class FacilityUpdate(BaseModel):
    facility_name: str

    model_config = {'from_attributes': True}
