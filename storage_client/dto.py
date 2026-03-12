from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime


class CustomerDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    companyName: str
    phone: str
    address: str
    email: str
    appUserId: str
    sales: Optional[List["SaleDto"]] = None
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, str):
            return int(v)
        return v


class LoginBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    userName: str
    password: str


class ProblemDetails(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    type: Optional[str] = None
    title: Optional[str] = None
    status: Optional[int] = None
    detail: Optional[str] = None
    instance: Optional[str] = None
    
    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v):
        if v is not None and isinstance(v, str):
            return int(v)
        return v


class ProductDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    productName: str
    price: float
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if isinstance(v, str):
            return int(v)
        return v
    
    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, v):
        if isinstance(v, str):
            return float(v)
        return v


class SaleUnitDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    amount: int
    productId: int
    price: float
    
    @field_validator('id', 'amount', 'productId', mode='before')
    @classmethod
    def validate_int_fields(cls, v):
        if isinstance(v, str):
            return int(v)
        return v
    
    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, v):
        if isinstance(v, str):
            return float(v)
        return v


class SaleDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    customerId: int
    realDate: Optional[datetime] = None  # ✅ Made optional
    plannedDate: Optional[datetime] = None  # ✅ Made optional
    saleUnits: Optional[List[SaleUnitDto]] = None
    
    @field_validator('id', 'customerId', mode='before')
    @classmethod
    def validate_int_fields(cls, v):
        if isinstance(v, str):
            return int(v)
        return v


class SupplierDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[int] = None
    companyName: str
    phone: str
    address: str
    email: str
    appUserId: str
    supplies: Optional[List["SupplyDto"]] = None
    
    @field_validator('id', mode='before')
    @classmethod
    def validate_id(cls, v):
        if v is not None and isinstance(v, str):
            return int(v)
        return v


class SupplyUnitDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    amount: int
    productId: int
    price: float
    
    @field_validator('id', 'amount', 'productId', mode='before')
    @classmethod
    def validate_int_fields(cls, v):
        if isinstance(v, str):
            return int(v)
        return v
    
    @field_validator('price', mode='before')
    @classmethod
    def validate_price(cls, v):
        if isinstance(v, str):
            return float(v)
        return v


class SupplyDto(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[int] = None
    supplierId: Optional[int] = None
    realDate: Optional[datetime] = None
    plannedDate: Optional[datetime] = None
    supplyUnits: Optional[List[SupplyUnitDto]] = None
    
    @field_validator('id', 'supplierId', mode='before')
    @classmethod
    def validate_int_fields(cls, v):
        if v is not None and isinstance(v, str):
            return int(v)
        return v


# ✅ Rebuild models with forward references
CustomerDto.model_rebuild()
SaleDto.model_rebuild()
SupplierDto.model_rebuild()
SupplyDto.model_rebuild()