from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.profiles.keyboards import back_to_main_kb
from handlers.profiles.api import ProfileAPIClient
from config import backend_link

api = ProfileAPIClient(backend_link)
profile_router = Router()


def format_workload_data(workload_type: str, data: dict) -> str:
    """Форматирует данные workload в красивый текст"""

    icons = {
        "oltp": "⚡",
        "olap": "📈",
        "mixed": "🔄",
        "iot": "🌐",
        "read_intensive": "📖",
        "write_intensive": "✍️",
        "web_service": "💻",
        "batch": "⚙️"
    }

    titles = {
        "oltp": "OLTP (Online Transaction Processing)",
        "olap": "OLAP (Online Analytical Processing)",
        "mixed": "Смешанный (Mixed OLTP/OLAP)",
        "iot": "IoT/Телеметрия",
        "read_intensive": "Read-Intensive (Чтение)",
        "write_intensive": "Write-Intensive (Запись)",
        "web_service": "Интерактивный веб-сервис",
        "batch": "Пакетная обработка (Batch Processing)"
    }

    icon = icons.get(workload_type, "📊")
    title = titles.get(workload_type, "Workload")

    # Форматируем метрики если они есть
    metrics_text = ""
    if data and isinstance(data, dict) and data.get("метрики"):
        metrics = data["метрики"]
        metrics_text = "📊 **Текущие метрики:**\n"
        for key, value in metrics.items():
            if key == "tps":
                metrics_text += f"• TPS: **{value}**\n"
            elif key == "latency_ms":
                metrics_text += f"• Задержка: **{value} ms**\n"
            elif key == "throughput_mb_sec":
                metrics_text += f"• Пропускная способность: **{value} MB/s**\n"
            elif key == "active_connections":
                metrics_text += f"• Активные подключения: **{value}**\n"
            elif key == "committed_percent":
                metrics_text += f"• Committed: **{value}%**\n"
            elif key == "temp_gb_per_hour":
                metrics_text += f"• Temp файлы: **{value} GB/час**\n"

    # Базовые описания для каждого типа workload
    descriptions = {
        "oltp": f"""
{metrics_text}
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
""",
        "olap": f"""
{metrics_text}
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
""",
        "mixed": f"""
{metrics_text}
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
""",
        "iot": f"""
{metrics_text}
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
""",
        "read_intensive": f"""
{metrics_text}
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
""",
        "write_intensive": f"""
{metrics_text}
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
""",
        "web_service": f"""
{metrics_text}
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
""",
        "batch": f"""
{metrics_text}
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
"""
    }

    return f"{icon} **{title}**\n\n{descriptions.get(workload_type, '')}"


@profile_router.callback_query(F.data == "workload_oltp")
async def handle_oltp(callback: CallbackQuery):
    """Обработчик для OLTP"""
    data = await api.oltp_work()
    description = format_workload_data("oltp", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_olap")
async def handle_olap(callback: CallbackQuery):
    """Обработчик для OLAP"""
    data = await api.olap_work()
    description = format_workload_data("olap", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_mixed")
async def handle_mixed(callback: CallbackQuery):
    """Обработчик для смешанной нагрузки"""
    data = await api.mixed_work()
    description = format_workload_data("mixed", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_iot")
async def handle_iot(callback: CallbackQuery):
    """Обработчик для IoT/Телеметрии"""
    data = await api.iot_work()
    description = format_workload_data("iot", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_read_intensive")
async def handle_read_intensive(callback: CallbackQuery):
    """Обработчик для Read-Intensive"""
    data = await api.read_intensive_work()
    description = format_workload_data("read_intensive", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_write_intensive")
async def handle_write_intensive(callback: CallbackQuery):
    """Обработчик для Write-Intensive"""
    data = await api.write_intensive_work()
    description = format_workload_data("write_intensive", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_web_service")
async def handle_web_service(callback: CallbackQuery):
    """Обработчик для интерактивного веб-сервиса"""
    data = await api.web_work()
    description = format_workload_data("web_service", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()


@profile_router.callback_query(F.data == "workload_batch")
async def handle_batch(callback: CallbackQuery):
    """Обработчик для пакетной обработки"""
    data = await api.batch_work()
    description = format_workload_data("batch", data)
    await callback.message.edit_text(description, reply_markup=back_to_main_kb())
    await callback.answer()