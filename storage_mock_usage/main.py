import schedule
import time
import logging
import signal
import random
from use_cases import UseCaseExecutor
from settings import (
    EXECUTION_INTERVAL_SECONDS,
    USE_CASE_PROBABILITIES,
    LOG_FILE,
    LOG_LEVEL,
    customer_usernames,
    supplier_usernames
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class SchedulerApp:
    def __init__(self):
        self.executor = UseCaseExecutor()
        self.running = True
        self.execution_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        logger.info("\nShutdown signal received. Stopping scheduler...")
        self.running = False
    
    def _select_use_case(self) -> str:
        """Select use case based on weighted probabilities"""
        use_cases = list(USE_CASE_PROBABILITIES.keys())
        weights = list(USE_CASE_PROBABILITIES.values())
        return random.choices(use_cases, weights=weights, k=1)[0]
    
    def _execute_use_case(self, use_case_name: str) -> bool:
        """Execute the selected use case"""
        method_map = {
            "staff_product_update": self.executor.staff_product_update,
            "customer_self_service": self.executor.customer_self_service,
            "supplier_self_service": self.executor.supplier_self_service,
        }
        
        method = method_map.get(use_case_name)
        if method:
            return method()
        else:
            logger.error(f"Unknown use case: {use_case_name}")
            return False
    
    def _run_scheduled_task(self):
        """Main scheduled task"""
        if not self.running:
            return
        
        self.execution_count += 1
        use_case = self._select_use_case()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Execution #{self.execution_count} | Use Case: {use_case}")
        logger.info(f"{'='*60}")
        
        start_time = time.time()
        success = self._execute_use_case(use_case)
        duration = time.time() - start_time
        
        if success:
            self.success_count += 1
            logger.info(f"✓ SUCCESS | Duration: {duration:.2f}s")
        else:
            self.failure_count += 1
            logger.warning(f"✗ FAILED | Duration: {duration:.2f}s")
        
        # Log statistics
        success_rate = (self.success_count / self.execution_count) * 100
        logger.info(f"Statistics - Success: {self.success_count}, Failed: {self.failure_count}, Rate: {success_rate:.1f}%")
    
    def run(self):
        """Start the scheduler"""
        logger.info("="*60)
        logger.info("DB Test Application Started")
        logger.info(f"Execution Interval: {EXECUTION_INTERVAL_SECONDS} seconds")
        logger.info(f"Use Case Probabilities: {USE_CASE_PROBABILITIES}")
        logger.info(f"Loaded {len(customer_usernames)} customers and {len(supplier_usernames)} suppliers")
        logger.info("="*60)

        # Schedule the task
        schedule.every(EXECUTION_INTERVAL_SECONDS).seconds.do(self._run_scheduled_task)
        
        # Run immediately on start
        logger.info("Running initial execution...")
        self._run_scheduled_task()
        
        # Main loop
        while self.running:
            schedule.run_pending()
            time.sleep(1)
        
        # Shutdown
        logger.info("\n" + "="*60)
        logger.info("Scheduler Stopped")
        logger.info(f"Total Executions: {self.execution_count}")
        logger.info(f"Successful: {self.success_count}")
        logger.info(f"Failed: {self.failure_count}")
        if self.execution_count > 0:
            logger.info(f"Success Rate: {(self.success_count/self.execution_count)*100:.1f}%")
        logger.info("="*60)


if __name__ == "__main__":
    app = SchedulerApp()
    app.run()