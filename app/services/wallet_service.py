from decimal import Decimal
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.wallet_repository import WalletRepository
from app.schemas.wallet import OperationType


class WalletNotFoundError(Exception):
    pass

class WalletAlreadyExistsError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass


class WalletService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = WalletRepository(session)

    async def create_wallet(
        self,
        wallet_id: UUID | None = None,
        balance: Decimal | None = None,
    ) -> dict:
        try:
            async with self.session.begin():
                wallet = await self.repository.create(wallet_id, balance)

                result = {
                    "wallet_id": wallet.id,
                    "balance": wallet.balance,
                }

            return result

        except IntegrityError as exc:
            raise WalletAlreadyExistsError() from exc

    async def get_balance(self, wallet_id: UUID) -> dict:
        wallet = await self.repository.get_by_id(wallet_id)

        if wallet is None:
            raise WalletNotFoundError()

        return {
            "wallet_id": wallet.id,
            "balance": wallet.balance,
        }

    async def process_operation(
        self,
        wallet_id: UUID,
        operation_type: OperationType,
        amount: Decimal,
    ) -> dict:

        async with self.session.begin():

            wallet = await self.repository.get_by_id(
                wallet_id,
                for_update=True,
            )

            if wallet is None:
                raise WalletNotFoundError()

            if operation_type == OperationType.DEPOSIT:
                wallet.balance += amount

            elif operation_type == OperationType.WITHDRAW:
                if wallet.balance < amount:
                    raise InsufficientFundsError()

                wallet.balance -= amount

            await self.session.flush()

            result = {
                "wallet_id": wallet.id,
                "balance": wallet.balance,
            }

        return result
