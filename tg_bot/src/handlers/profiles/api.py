import aiohttp
from typing import Dict, Any


class ProfileAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Базовый метод для выполнения запросов"""
        if not self.session:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    return await response.json()
        else:
            async with self.session.get(f"{self.base_url}{endpoint}") as response:
                return await response.json()

    # OLTP профиль
    async def oltp_work(self) -> Dict[str, Any]:
        return await self._make_request("/oltp_work")

    # OLAP профиль
    async def olap_work(self) -> Dict[str, Any]:
        return await self._make_request("/olap_work")

    # Mixed профиль
    async def mixed_work(self) -> Dict[str, Any]:
        return await self._make_request("/mixed_work")

    # IoT профиль
    async def iot_work(self) -> Dict[str, Any]:
        return await self._make_request("/iot_work")

    # Read-Intensive профиль
    async def read_intensive_work(self) -> Dict[str, Any]:
        return await self._make_request("/read_intensive_work")

    # Write-Intensive профиль
    async def write_intensive_work(self) -> Dict[str, Any]:
        return await self._make_request("/write_intensive_work")

    # Web Service профиль
    async def web_work(self) -> Dict[str, Any]:
        return await self._make_request("/web_work")

    # Batch Processing профиль
    async def batch_work(self) -> Dict[str, Any]:
        return await self._make_request("/batch_work")

    # Массовый запрос всех профилей
    async def get_all_profiles(self) -> Dict[str, Any]:
        """Получить данные всех профилей одновременно"""
        endpoints = {
            "oltp": "/oltp_work",
            "olap": "/olap_work",
            "mixed": "/mixed_work",
            "iot": "/iot_work",
            "read_intensive": "/read_intensive_work",
            "web": "/web_work",
            "batch": "/batch_work"
        }

        results = {}
        for profile_name, endpoint in endpoints.items():
            try:
                results[profile_name] = await self._make_request(endpoint)
            except Exception as e:
                results[profile_name] = {"error": str(e)}

        return results