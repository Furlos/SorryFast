from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="OLTP (Online Transaction Processing)",
                callback_data="workload_oltp"
            )],
            [InlineKeyboardButton(
                text="OLAP (Online Analytical Processing)",
                callback_data="workload_olap"
            )],
            [InlineKeyboardButton(
                text="Смешанный (Mixed OLTP/OLAP)",
                callback_data="workload_mixed"
            )],
            [InlineKeyboardButton(
                text="IoT/Телеметрия",
                callback_data="workload_iot"
            )],
            [InlineKeyboardButton(
                text="Read-Intensive (Чтение)",
                callback_data="workload_read_intensive"
            )],
            [InlineKeyboardButton(
                text="Write-Intensive (Запись)",
                callback_data="workload_write_intensive"
            )],
            [InlineKeyboardButton(
                text="Интерактивный веб-сервис",
                callback_data="workload_web_service"
            )],
            [InlineKeyboardButton(
                text="Пакетная обработка (Batch Processing)",
                callback_data="workload_batch"
            )],
        ]
    )