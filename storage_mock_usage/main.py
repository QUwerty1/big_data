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

# Настройка логирования
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

        # Настройка обработчиков сигналов для корректного завершения
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        logger.info("\nПолучен сигнал завершения. Остановка планировщика...")
        self.running = False

    def _select_use_case(self) -> str:
        """Выбрать сценарий на основе взвешенных вероятностей"""
        use_cases = list(USE_CASE_PROBABILITIES.keys())
        weights = list(USE_CASE_PROBABILITIES.values())
        return random.choices(use_cases, weights=weights, k=1)[0]

    def _execute_use_case(self, use_case_name: str) -> bool:
        """Выполнить выбранный сценарий"""
        method_map = {
            "staff_get_all_products": self.executor.staff_get_all_products,
            "staff_get_sale_details": self.executor.staff_get_sale_details,
            "staff_get_supply_details": self.executor.staff_get_supply_details,
            "customer_get_own_sales": self.executor.customer_get_own_sales,
            "customer_get_own_sale": self.executor.customer_get_own_sale,
            "supplier_get_own_supplies": self.executor.supplier_get_own_supplies,
            "supplier_get_own_supply": self.executor.supplier_get_own_supply,
            "staff_create_sale": self.executor.staff_create_sale,
            "staff_create_supply": self.executor.staff_create_supply,
            "staff_get_all_sales": self.executor.staff_get_all_sales,
        }

        method = method_map.get(use_case_name)
        if method:
            return method()
        else:
            logger.error(f"Неизвестный сценарий: {use_case_name}")
            return False

    def _run_scheduled_task(self):
        """Основная задача по расписанию"""
        if not self.running:
            return

        self.execution_count += 1
        use_case = self._select_use_case()

        logger.info(f"\n{'='*60}")
        logger.info(f"Выполнение #{self.execution_count} | Сценарий: {use_case}")
        logger.info(f"{'='*60}")

        start_time = time.time()
        success = self._execute_use_case(use_case)
        duration = time.time() - start_time

        if success:
            self.success_count += 1
            logger.info(f"✓ УСПЕХ | Длительность: {duration:.2f}с")
        else:
            self.failure_count += 1
            logger.warning(f"✗ НЕУДАЧА | Длительность: {duration:.2f}с")

        # Логирование статистики
        success_rate = (self.success_count / self.execution_count) * 100
        logger.info(f"Статистика - Успехов: {self.success_count}, Неудач: {self.failure_count}, Процент: {success_rate:.1f}%")

    def run(self):
        """Запустить планировщик"""
        logger.info("="*60)
        logger.info("Приложение тестирования БД запущено")
        logger.info(f"Интервал выполнения: {EXECUTION_INTERVAL_SECONDS} секунд")
        logger.info(f"Вероятности сценариев: {USE_CASE_PROBABILITIES}")
        logger.info(f"Загружено {len(customer_usernames)} клиентов и {len(supplier_usernames)} поставщиков")
        logger.info("="*60)

        # Запланировать задачу
        schedule.every(EXECUTION_INTERVAL_SECONDS).seconds.do(self._run_scheduled_task)

        # Выполнить сразу при запуске
        logger.info("Выполнение начального запуска...")
        self._run_scheduled_task()

        # Основной цикл
        while self.running:
            schedule.run_pending()
            time.sleep(1)

        # Завершение
        logger.info("\n" + "="*60)
        logger.info("Планировщик остановлен")
        logger.info(f"Всего выполнений: {self.execution_count}")
        logger.info(f"Успешно: {self.success_count}")
        logger.info(f"Неудачно: {self.failure_count}")
        if self.execution_count > 0:
            logger.info(f"Процент успеха: {(self.success_count/self.execution_count)*100:.1f}%")
        logger.info("="*60)


if __name__ == "__main__":
    app = SchedulerApp()
    app.run()
