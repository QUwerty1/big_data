from pydantic import BaseModel, Field
from typing import Optional, List, Union
from datetime import datetime

class ProblemDetails(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    status: Optional[int] = None
    detail: Optional[str] = None
    instance: Optional[str] = None

class LoginBody(BaseModel):
    userName: str
    password: str

class NewCustomer(BaseModel):
    companyName: str
    phone: str
    address: str
    email: str

class CustomerDto(BaseModel):
    id: int
    companyName: str
    phone: str
    address: str
    email: str
    appUserId: str
    sales: Optional[List['SaleDto']] = []

class NewSupplier(BaseModel):
    companyName: str
    phone: str
    address: str
    email: str

class SupplierDto(BaseModel):
    id: Optional[int] = None
    companyName: str
    phone: str
    address: str
    email: str
    appUserId: Optional[str] = None
    supplies: Optional[List['SupplyDto']] = []

class ProductDto(BaseModel):
    id: Optional[int] = None
    productName: str
    price: float

class SaleUnitDto(BaseModel):
    id: Optional[int] = None
    amount: int
    productId: int
    price: float

class SupplyUnitDto(BaseModel):
    id: Optional[int] = None
    amount: int
    productId: int
    price: float

class SaleViewDto(BaseModel):
    id: Optional[int] = None
    customerId: int
    realDate: Optional[str] = None
    plannedDate: Optional[str] = None
    saleUnitIds: Optional[List[int]] = []

class SupplyViewDto(BaseModel):
    id: Optional[int] = None
    supplierId: Optional[int] = None
    realDate: Optional[str] = None
    plannedDate: Optional[str] = None
    supplyUnitIds: Optional[List[int]] = []

class SaleDto(BaseModel):
    id: Optional[int] = None
    customerId: int
    realDate: Optional[str] = None
    plannedDate: Optional[str] = None
    saleUnits: Optional[List[SaleUnitDto]] = []

class SupplyDto(BaseModel):
    id: Optional[int] = None
    supplierId: Optional[int] = None
    realDate: Optional[str] = None
    plannedDate: Optional[str] = None
    supplyUnits: Optional[List[SupplyUnitDto]] = []

# Update forward references
CustomerDto.model_rebuild()
SupplierDto.model_rebuild()