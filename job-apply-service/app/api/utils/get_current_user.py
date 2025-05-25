from fastapi import HTTPException, status, Header
from typing import Optional


def get_current_user(
        x_user_id: Optional[str] = Header(None),
        x_user_email: Optional[str] = Header(None)
) -> dict:
    """
    Extract user info from Kong gateway headers.
    Kong should pass user info via headers after authentication.
    """
    if not x_user_id or not x_user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User authentication headers missing"
        )

    try:
        user_id = int(x_user_id)
        return {"user_id": user_id, "user_email": x_user_email}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )