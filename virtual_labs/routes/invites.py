from typing import Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from virtual_labs.core.exceptions.api_error import VliError
from virtual_labs.core.types import VliAppResponse
from virtual_labs.domain.invite import InviteOut
from virtual_labs.infrastructure.db.config import default_session_factory
from virtual_labs.infrastructure.email.email_utils import InviteOrigin
from virtual_labs.infrastructure.kc.auth import verify_jwt
from virtual_labs.infrastructure.kc.models import AuthUser
from virtual_labs.infrastructure.settings import settings
from virtual_labs.usecases import invites as invite_cases

router = APIRouter(
    prefix="/invites",
    tags=["Invites"],
)


@router.post(
    "/test",
    operation_id="invite_handler_test",
    summary="This will process the invite (add users to groups, update the invite status)",
    response_model=None,
    include_in_schema=settings.DEPLOYMENT_ENV != "production",
)
async def handle_test_invite(
    invite_id: UUID,
    origin: InviteOrigin,
    session: Session = Depends(default_session_factory),
    auth: Tuple[AuthUser, str] = Depends(verify_jwt),
) -> Response | VliError:
    return await invite_cases.invitation_handler_test(
        session, invite_id=invite_id, origin=origin
    )


@router.post(
    "",
    operation_id="invite_handler",
    summary="This will process the invite (add users to groups, update the invite status)",
    response_model=VliAppResponse[InviteOut],
)
async def handle_invite(
    session: Session = Depends(default_session_factory),
    token: str = Query("", description="invitation token"),
    auth: Tuple[AuthUser, str] = Depends(verify_jwt),
) -> Response | VliError:
    return await invite_cases.invitation_handler(
        session,
        invite_token=token,
        auth=auth,
    )
