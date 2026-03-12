from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from typing import Optional, Any, Dict, List, Type, TypeVar, Union, get_args, get_origin

import requests
from urllib.parse import urljoin

from config import get_api_url, get_token_file
from dto import (
    CustomerDto, ProductDto, SaleDto, SupplierDto, SupplyDto,
    LoginBody, ProblemDetails
)

class ApiError(Exception):
    """API error exception"""
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 problem: Optional[ProblemDetails] = None):
        super().__init__(message)
        self.status_code = status_code
        self.problem = problem


T = TypeVar('T')


class ApiClient:
    """HTTP client for the StorageServer API"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or get_api_url()
        if not self.base_url.endswith('/'):
            self.base_url += '/'
        
        self.session = requests.Session()
        self.token: Optional[str] = self._load_token()
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        if self.token:
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
    
    def _load_token(self) -> Optional[str]:
        token_file = Path(get_token_file())
        if token_file.exists():
            return token_file.read_text().strip()
        return None
    
    def _save_token(self, token: str) -> None:
        Path(get_token_file()).write_text(token)
    
    def _clear_token(self) -> None:
        self.token = None
        self.session.headers.pop('Authorization', None)
        token_file = Path(get_token_file())
        if token_file.exists():
            token_file.unlink()
    
    def _build_url(self, path: str) -> str:
        return urljoin(self.base_url, path if path.startswith('/') else '/' + path)
    
    def _handle_response(self, response: requests.Response, 
                        response_model: Optional[Type[T]] = None) -> Union[T, Any]:
        if response.status_code >= 400:
            # ✅ Safely parse error response
            try:
                error_data = response.json()
                # ✅ Check if it's a dict before unpacking
                if isinstance(error_data, dict):
                    problem = ProblemDetails(**error_data)
                    raise ApiError(f"API Error: {problem.title or 'Unknown error'}", 
                                 status_code=response.status_code, 
                                 problem=problem)
                else:
                    # ✅ Handle string or other non-dict responses
                    raise ApiError(f"API Error: {str(error_data)}", 
                                 status_code=response.status_code)
            except (ValueError, KeyError):
                # ✅ Handle non-JSON responses
                error_text = response.text.strip() or f"HTTP {response.status_code}"
                raise ApiError(f"API Error: {error_text}", 
                             status_code=response.status_code)
        
        if response.status_code == 204 or not response.content:
            return None
        
        if response_model:
            data = response.json()
            
            origin = get_origin(response_model)
            if origin is list:
                args = get_args(response_model)
                if args:
                    item_type = args[0]
                    if isinstance(item_type, type) and issubclass(item_type, BaseModel):
                        return [item_type.model_validate(item) for item in data]
                    else:
                        return data
            
            if response_model in (bool, str, int, float):
                return data
            
            if isinstance(response_model, type) and issubclass(response_model, BaseModel):
                return response_model.model_validate(data)
            
            return response_model(**data)
        
        return response.json() if response.content else None
    
    
    def _to_dict(self, data: Any) -> Any:
        """Convert Pydantic model to dict."""
        if data and hasattr(data, 'model_dump'):
            return data.model_dump(exclude_none=True, by_alias=True)
        return data
    
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Any] = None,
        response_model: Optional[Type[T]] = None,
        **kwargs
    ) -> Union[T, Any]:
        url = self._build_url(path)
        
        data = self._to_dict(data)
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=data,
            **kwargs
        )
        
        return self._handle_response(response, response_model)
    
    def login(self, username: str, password: str) -> str:
        login_data = LoginBody(userName=username, password=password)
        url = self._build_url('/user/login')
        
        response = self.session.post(
            url=url,
            json=self._to_dict(login_data)
        )
        
        if response.status_code == 200:
            token = response.text.strip('"')
            self.token = token
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            self._save_token(self.token)
            return self.token
        
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                problem = ProblemDetails(**error_data)
                raise ApiError(f"Login failed: {problem.title}", 
                             status_code=response.status_code, 
                             problem=problem)
            else:
                raise ApiError(f"Login failed: {str(error_data)}", 
                             status_code=response.status_code)
        except (ValueError, KeyError):
            error_text = response.text.strip() or f"HTTP {response.status_code}"
            raise ApiError(f"Login failed: {error_text}", 
                         status_code=response.status_code)
        
        raise ApiError("Login failed: Unknown error")
    
    def logout(self) -> None:
        self._clear_token()
    
    def register(self, username: str, password: str) -> None:
        login_data = LoginBody(userName=username, password=password)
        self.request('POST', '/user/register', data=login_data)
    
    def is_staff(self) -> bool:
        return self.request('GET', '/user/is_staff', response_model=bool)
    
    def get_customer(self, customer_id: int) -> CustomerDto:
        return self.request('GET', f'/customer/{customer_id}', response_model=CustomerDto)
    
    def get_all_customers(self, take: Optional[int] = None, skip: int = 0) -> List[CustomerDto]:
        params = {'skip': skip}
        if take is not None:
            params['take'] = take
        return self.request('GET', '/customer', params=params, 
                          response_model=List[CustomerDto])
    
    def create_customer(self, customer: CustomerDto) -> CustomerDto:
        return self.request('POST', '/customer', data=customer, response_model=CustomerDto)
    
    def get_me_customer(self) -> CustomerDto:
        return self.request('GET', '/customer/me', response_model=CustomerDto)
    
    def get_product(self, product_id: int) -> ProductDto:
        return self.request('GET', f'/product/{product_id}', response_model=ProductDto)
    
    def get_all_products(self) -> List[ProductDto]:
        return self.request('GET', '/product', response_model=List[ProductDto])
    
    def create_product(self, product: ProductDto) -> ProductDto:
        return self.request('POST', '/product', data=product, response_model=ProductDto)
    
    def update_product(self, product: ProductDto) -> ProductDto:
        return self.request('PUT', '/product', data=product, response_model=ProductDto)
    
    def get_sale(self, sale_id: int) -> SaleDto:
        return self.request('GET', f'/sale/{sale_id}', response_model=SaleDto)
    
    def get_all_sales(self) -> List[SaleDto]:
        return self.request('GET', '/sale', response_model=List[SaleDto])
    
    def create_sale(self, sale: SaleDto) -> SaleDto:
        return self.request('POST', '/sale', data=sale, response_model=SaleDto)
    
    def update_sale(self, sale: SaleDto) -> SaleDto:
        return self.request('PUT', '/sale', data=sale, response_model=SaleDto)
    
    def get_supplier(self, supplier_id: int) -> SupplierDto:
        return self.request('GET', f'/supplier/{supplier_id}', response_model=SupplierDto)
    
    def get_all_suppliers(self, take: Optional[int] = None, skip: int = 0) -> List[SupplierDto]:
        params = {'skip': skip}
        if take is not None:
            params['take'] = take
        return self.request('GET', '/supplier', params=params, 
                          response_model=List[SupplierDto])
    
    def create_supplier(self, supplier: SupplierDto) -> SupplierDto:
        return self.request('POST', '/supplier', data=supplier, response_model=SupplierDto)
    
    def get_me_supplier(self) -> SupplierDto:
        return self.request('GET', '/supplier/me', response_model=SupplierDto)
    
    def get_supply(self, supply_id: int) -> SupplyDto:
        return self.request('GET', f'/supply/{supply_id}', response_model=SupplyDto)
    
    def get_all_supplies(self) -> List[SupplyDto]:
        return self.request('GET', '/supply', response_model=List[SupplyDto])
    
    def create_supply(self, supply: SupplyDto) -> SupplyDto:
        return self.request('POST', '/supply', data=supply, response_model=SupplyDto)
    
    def update_supply(self, supply: SupplyDto) -> SupplyDto:
        return self.request('PUT', '/supply', data=supply, response_model=SupplyDto)
    
    def generate_users(self, count: int = 1) -> List[str]:
        return self.request('POST', '/generator/users', params={'count': count}, 
                          response_model=List[str])

    def generate_customers(self, count: int = 1) -> List[CustomerDto]:
        return self.request('POST', '/generator/customers', params={'count': count}, 
                          response_model=List[CustomerDto])

    def generate_suppliers(self, count: int = 1) -> List[SupplierDto]:
        return self.request('POST', '/generator/suppliers', params={'count': count}, 
                          response_model=List[SupplierDto])

    def generate_products(self, count: int = 1, min_price: float = 1, 
                         max_price: float = 1000000) -> List[ProductDto]:
        params = {
            'count': count,
            'minPrice': min_price,
            'maxPrice': max_price
        }
        return self.request('POST', '/generator/products', params=params, 
                          response_model=List[ProductDto])

    def generate_sales(self, count: int = 1, min_date: Optional[datetime] = None, 
                      max_date: Optional[datetime] = None) -> List[SaleDto]:
        params: Dict[str, Any] = {'count': count}
        
        if min_date is not None:
            params['minDate'] = min_date.isoformat() if isinstance(min_date, datetime) else str(min_date)
                
        if max_date is not None:
            params['maxDate'] = max_date.isoformat() if isinstance(max_date, datetime) else str(max_date)
        
        return self.request('POST', '/generator/sales', params=params, 
                          response_model=List[SaleDto])
    
    def test_private(self) -> None:
        self.request('GET', '/test/private')
    
    def test_public(self) -> None:
        self.request('GET', '/test/public')
    
    def test_staff(self) -> None:
        self.request('GET', '/test/staff')