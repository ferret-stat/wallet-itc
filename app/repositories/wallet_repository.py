from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Wallet


class WalletRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        wallet_id: UUID,
        for_update: bool = False,
    ) -> Wallet | None:
        stmt = select(Wallet).where(
            Wallet.id == wallet_id
        )
        # Блокировка при чтении
        if for_update:
            stmt = stmt.with_for_update()

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()
