from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards import back_to_main_kb
from api import (
    ProfileAPIClient
)
from ...config import backend_link
api = ProfileAPIClient(backend_link)
profile_router = Router()


@profile_router.callback_query(F.data == "workload_oltp")
async def handle_oltp(callback: CallbackQuery):
    """Обработчик для OLTP"""

    description = f"""
⚡ **OLTP (Online Transaction Processing)**


**Данные: {api.oltp_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 85-95% (короткие транзакции)
• DB Time Committed: 70-80%
• TPS: > 100 (переход в Mixed при >2000 TPS)
• Время запроса: < 100ms
• Активные сессии: 50-200

**🔧 Ключевые параметры PostgreSQL:**
• temp_file_limit: 5% от /pg_data
• checkpoint_timeout: 900s
• min_wal_size: 2048 MB
• max_wal_size: 8192 MB
• max_parallel_workers_per_gather: 0
• max_parallel_workers: 0
• shared_buffers: 25% RAM
• work_mem: 4-8MB

**🏢 Бизнес-примеры:**
• Банковские терминалы и переводы
• Биржевые торги
• Системы бронирования
• Онлайн-платежи

**🔄 Переходные состояния:**
• OLTP → Mixed: при TPS > 2000 + аналитические запросы
• OLTP → OLAP: при снятии OLTP нагрузки + работающие тяжелые запросы

**📈 Экспериментальные данные (pgbench TPC-B):**
• TPS: 1500-2000
• Latency: 2-5ms
• Throughput: 1.5M операций/час
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_olap")
async def handle_olap(callback: CallbackQuery):
    """Обработчик для OLAP"""
    description = f"""
📈 **OLAP (Online Analytical Processing)**

**Данные: {api.olap_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 40-50% (длительные операции)
• DB Time Committed: 30-40%
• TPS: < 5
• Время запроса: > 10s
• Объем данных на запрос: гигабайты

**🔧 Ключевые параметры PostgreSQL:**
• temp_file_limit: 10% от /pg_data
• checkpoint_timeout: 1800s
• min_wal_size: 4096 MB
• max_wal_size: 16384 MB
• max_parallel_workers_per_gather: CPU/4
• max_parallel_workers: CPU/2
• work_mem: 64-256MB
• shared_buffers: 40-60% RAM

**🏢 Бизнес-примеры:**
• BI-системы и отчетность
• Data Mining и аналитика
• Годовые отчеты
• Бизнес-аналитика

**🔄 Переходные состояния:**
• OLAP → Mixed: при параллельном запуске OLTP нагрузки
• OLAP → OLTP: при преобладании коротких транзакций

**📈 Экспериментальные данные:**
• Время выполнения: 10-30s
• CPU utilization: 80-95%
• Memory usage: 60-80%
• Ускорение с parallel query: 3-4x
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_mixed")
async def handle_mixed(callback: CallbackQuery):
    """Обработчик для смешанной нагрузки"""

    description = f"""
🔄 **Смешанный (Mixed OLTP/OLAP)**

**Данные: {api.mixed_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 60-70%
• DB Time Committed: 50-60%
• TPS: 10-50
• Время запроса: 0.1-5s
• Соотношение OLTP/OLAP: 40-60%/40-60%

**🔧 Ключевые параметры PostgreSQL:**
• work_mem: 8-32MB
• maintenance_work_mem: 1-2GB
• effective_cache_size: 50% RAM
• max_connections: 100-300
• shared_buffers: 30-40% RAM

**🏢 Бизнес-примеры:**
• E-commerce с аналитикой в реальном времени
• CRM системы
• SaaS приложения
• Финансовые платформы

**🔄 Балансировка нагрузок:**
• Горячие/холодные данные
• Read replicas для аналитики
• Resource groups для изоляции
• Connection pooling

**📈 Производительность:**
• 40-60% от пиковой производительности OLTP
• 2-3x ускорение vs однопоточный режим
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_iot")
async def handle_iot(callback: CallbackQuery):
    """Обработчик для IoT/Телеметрии"""

    description = f"""
🌐 **IoT/Телеметрия**

**Данные: {api.iot_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 90-95% (массовая запись)
• DB Time Committed: 80-90%
• TPS: > 500 (до 10000+ для крупных систем)
• Операции INSERT: > 90%
• Рост данных: быстрый (GB/час)

**🔧 Ключевые параметры PostgreSQL:**
• max_wal_size: 4-8GB
• checkpoint_timeout: 30-60min
• autovacuum_vacuum_scale_factor: 0.1
• wal_buffers: 64-256MB
• shared_buffers: 20-30% RAM

**🏢 Бизнес-примеры:**
• Умные устройства и сенсорные сети
• Мониторинг оборудования
• Промышленная телеметрия
• Системы сбора метрик

**💡 Специализированные решения:**
• TimescaleDB для временных рядов
• BRIN индексы вместо B-tree
• UNLOGGED таблицы для временных данных
• Compression policies

**📈 Производительность:**
• Пропускная способность: 10K+ записей/сек
• Эффективное сжатие: 70-90%
• Оптимизировано для массовых операций
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_read_intensive")
async def handle_read_intensive(callback: CallbackQuery):
    """Обработчик для Read-Intensive"""

    description = f"""
📖 **Read-Intensive (Чтение)**

**Данные: {api.read_intensive_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 70-80% (операции чтения)
• DB Time Committed: 60-70%
• Соотношение read/write: > 80/20
• Cache hit ratio: > 95%
• Время ответа: < 200ms

**🔧 Ключевые параметры PostgreSQL:**
• shared_buffers: 25-40% RAM
• effective_cache_size: 80% RAM
• random_page_cost: 1.1 (для SSD)
• work_mem: 16-64MB
• maintenance_work_mem: 1-2GB

**🏢 Бизнес-примеры:**
• Каталоги товаров и CMS системы
• Справочники и энциклопедии
• Блоги и медиа-порталы
• Системы документооборота

**🚀 Стратегии оптимизации:**
• Активные индексы (B-tree, GIN, GIST)
• Read replicas для масштабирования
• Query cache и кэширование
• Covering индексы

**📈 Производительность:**
• Быстрое время отклика: < 200ms
• Эффективное использование кэша
• Легко масштабируется репликацией
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_write_intensive")
async def handle_write_intensive(callback: CallbackQuery):
    """Обработчик для Write-Intensive"""
    description = f"""
✍️ **Write-Intensive (Запись)**

**Данные: {api.write_intensive_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 85-95% (операции записи)
• DB Time Committed: 75-85%
• Соотношение read/write: < 20/80
• WAL usage: высокий
• Vacuum activity: высокая

**🔧 Ключевые параметры PostgreSQL:**
• wal_buffers: 64-256MB
• checkpoint_timeout: 30-60min
• max_wal_size: 4-8GB
• autovacuum_vacuum_scale_factor: 0.05
• shared_buffers: 20-30% RAM

**🏢 Бизнес-примеры:**
• Системы логирования и аудита
• Сбор метрик и мониторинг
• Очереди сообщений
• Системы обработки событий

**⚡ Оптимизация записи:**
• Минимизация индексов
• Batch INSERT для группировки
• UNLOGGED таблицы
• Tablespaces на быстрых дисках

**📈 Производительность:**
• Высокая пропускная способность записи
• Эффективное использование WAL
• Оптимизировано для последовательных операций
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_web_service")
async def handle_web_service(callback: CallbackQuery):
    """Обработчик для интерактивного веб-сервиса"""

    description = f"""
💻 **Интерактивный веб-сервис**

**Данные: {api.web_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 80-90% (высокая конкурентность)
• DB Time Committed: 70-80%
• Активные подключения: > 50
• Время ответа: < 500ms
• Query complexity: низкая-средняя

**🔧 Ключевые параметры PostgreSQL:**
• max_connections: 200-500
• shared_buffers: 25% RAM
• work_mem: 4-8MB
• random_page_cost: 1.1
• effective_cache_size: 75% RAM

**🏢 Бизнес-примеры:**
• Социальные сети и мессенджеры
• SaaS приложения
• Онлайн-маркетплейсы
• CRM и ERP системы

**🔗 Управление подключениями:**
• PgBouncer для connection pooling
• READ COMMITTED уровень изоляции
• Балансировка нагрузки
• Мониторинг "горячих" строк

**📈 Производительность:**
• Быстрое время отклика: < 500ms
• Хорошая масштабируемость по подключениям
• Поддержка высокой доступности
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_batch")
async def handle_batch(callback: CallbackQuery):
    """Обработчик для пакетной обработки"""

    description = f"""
⚙️ **Пакетная обработка (Batch Processing)**

**Данные: {api.batch_work()}**

**📊 Метрики DB Time и производительности:**
• DB Time ASH: 50-70% (длительные операции)
• DB Time Committed: 40-60%
• Длительность операций: минуты-часы
• CPU utilization: высокая
• Memory usage: высокая

**🔧 Ключевые параметры PostgreSQL:**
• maintenance_work_mem: 2-4GB
• work_mem: 128-512MB
• temp_buffers: 32-128MB
• max_parallel_workers: 4-8
• autovacuum_naptime: 10s

**🏢 Бизнес-примеры:**
• ETL процессы и трансформации данных
• Ночные расчеты и отчетность
• Массовые обновления данных
• Генерация аналитических витрин

**🕒 Стратегии выполнения:**
• Chunk processing для больших объемов
• Parallel execution
• Staging tables
• Выполнение в непиковое время

**📈 Производительность:**
• Эффективная обработка больших объемов
• Оптимальное использование ресурсов
• Возможность сложных преобразований
• Пакетная оптимизация операций
"""

    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()