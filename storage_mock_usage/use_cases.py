# use_cases.py
# Implementation of all use cases

import random
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from api_client import APIClient
from settings import (
    STAFF_CREDENTIALS,
    CUSTOMER_CREDENTIALS,
    SUPPLIER_CREDENTIALS,
    PRICE_VARIATION_PERCENT
)

logger = logging.getLogger(__name__)


class UseCaseExecutor:
    def __init__(self):
        self.client = APIClient()
    
    def _get_random_credentials(self, credentials_list: List[Dict[str, str]]) -> Dict[str, str]:
        return random.choice(credentials_list)
    
    def _calculate_new_price(self, current_price: float) -> float:
        """Calculate new price with ±20% variation"""
        variation = random.uniform(-PRICE_VARIATION_PERCENT, PRICE_VARIATION_PERCENT)
        new_price = current_price * (1 + variation / 100)
        return round(new_price, 2)
    
    def _get_random_item(self, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if items:
            return random.choice(items)
        return None
    
    # UC01: Staff Product Update
    def staff_product_update(self) -> bool:
        """Staff modifies existing product pricing"""
        logger.info("Executing UC01: Staff Product Update")
        
        # Step 1: Login as Staff
        creds = self._get_random_credentials(STAFF_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC01 Step 1 Failed: Staff login")
            return False
        
        try:
            # Step 2: Get products list
            products = self.client.get_products()
            if not products:
                logger.warning("UC01 Step 2 Failed: No products available")
                return False
            
            # Step 3: Select and update product price
            product = self._get_random_item(products)
            if product is None or "id" not in product or "price" not in product:
                logger.warning("UC01 Step 3 Failed: Invalid product data")
                return False
            
            current_price = product.get("price", 100)
            if not isinstance(current_price, (int, float)):
                logger.warning("UC01 Step 3 Failed: Invalid price type")
                return False
            
            new_price = self._calculate_new_price(float(current_price))
            product["price"] = new_price
            
            if not self.client.update_product(product):
                logger.error("UC01 Step 3 Failed: Product update")
                return False
            
            # Step 4: Verify change
            updated_product = self.client.get_product(product["id"])
            if updated_product and abs(float(updated_product.get("price", 0)) - new_price) < 0.01:
                logger.info(f"UC01 Success: Product {product['id']} price updated to {new_price}")
                return True
            
            logger.error("UC01 Step 4 Failed: Verification")
            return False
        finally:
            self.client.logout()
    
    # UC02: Customer Self-Service View
    def customer_self_service(self) -> bool:
        """Customer checks profile and transaction history"""
        logger.info("Executing UC02: Customer Self-Service")
        
        # Step 1: Login as Customer
        creds = self._get_random_credentials(CUSTOMER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC02 Step 1 Failed: Customer login")
            return False
        
        try:
            # Step 2: Fetch profile
            profile = self.client.get_customer_me()
            if profile is None:
                logger.warning("UC02 Step 2 Failed: Could not fetch profile")
                return False
            
            # Step 3: Fetch own sales
            sales = self.client.get_sale_me()
            logger.info(f"UC02 Step 3: Found {len(sales)} sales for customer")
            
            # Step 4: Verify session
            user_info = self.client.get_user_me()
            if user_info:
                logger.info(f"UC02 Success: Customer {creds['username']} session verified")
                return True
            
            logger.error("UC02 Step 4 Failed: Session verification")
            return False
        finally:
            self.client.logout()
    
    # UC03: Supplier Self-Service
    def supplier_self_service(self) -> bool:
        """Supplier checks profile and supply list"""
        logger.info("Executing UC03: Supplier Self-Service")
        
        # Step 1: Login as Supplier
        creds = self._get_random_credentials(SUPPLIER_CREDENTIALS)
        if not self.client.login(creds["username"], creds["password"]):
            logger.error("UC03 Step 1 Failed: Supplier login")
            return False
        
        try:
            # Step 2: Fetch profile
            profile = self.client.get_supplier_me()
            if profile is None:
                logger.warning("UC03 Step 2 Failed: Could not fetch profile")
                return False
            
            # Step 3: Fetch all supplies
            supplies = self.client.get_supplies()
            logger.info(f"UC03 Step 3: Found {len(supplies)} supplies")
            
            # Step 4: Verify session
            user_info = self.client.get_user_me()
            if user_info:
                logger.info(f"UC03 Success: Supplier {creds['username']} session verified")
                return True
            
            logger.error("UC03 Step 4 Failed: Session verification")
            return False
        finally:
            self.client.logout()