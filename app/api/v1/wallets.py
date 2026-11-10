from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_api_key
from app.database.db import get_db
from app.schemas.wallet import (
    WalletOperationRequest,
    WalletOperationResponse,
    WalletResponse,
    WalletCreateRequest,
)
from app.services.wallet_service import (
    InsufficientFundsError,
    WalletAlreadyExistsError,
    WalletNotFoundError,
    WalletService,
)


router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"],
    dependencies=[Depends(require_api_key)],
)
@router.post(
    "/create",
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
    request: WalletCreateRequest,
    session: AsyncSession = Depends(get_db),
):
    service = WalletService(session)

    try:
        return await service.create_wallet(request.wallet_id, request.balance)
    except WalletAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wallet already exists"
        )


@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
)
async def get_wallet(
    wallet_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    service = WalletService(session)

    try:
        return await service.get_balance(wallet_id)

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )


@router.post(
    "/{wallet_id}/operation",
    response_model=WalletOperationResponse,
)
async def process_wallet_operation(
    wallet_id: UUID,
    request: WalletOperationRequest,
    session: AsyncSession = Depends(get_db),
):
    service = WalletService(session)

    try:
        return await service.process_operation(
            wallet_id=wallet_id,
            operation_type=request.operation_type,
            amount=request.amount,
        )

    except WalletNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet not found",
        )

    except InsufficientFundsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Insufficient funds",
        )
