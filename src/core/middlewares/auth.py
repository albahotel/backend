from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from litestar.connection import ASGIConnection
from litestar.middleware import AbstractMiddleware, AuthenticationResult
from litestar.exceptions import NotAuthorizedException, PermissionDeniedException

from datetime import datetime

from src.core.models import Token


class AuthMiddleware(AbstractMiddleware):
    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        auth_header = connection.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise NotAuthorizedException("Missing or invalid authorization header")

        token_value = auth_header[7:]
        session: AsyncSession = connection.app.dependencies["db_session"].dependency()  # type: ignore

        token = await session.scalar(select(Token).where(Token.token == token_value))

        if not token or token.expires_at < datetime.now():
            raise NotAuthorizedException("Invalid or expired token")

        if connection.url.path.startswith("/api") and not token.is_admin:
            raise PermissionDeniedException("Admin access required")

        connection.state.token = token
        return AuthenticationResult(user=None, auth=token)
