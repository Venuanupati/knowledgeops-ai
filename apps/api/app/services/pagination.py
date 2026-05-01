from fastapi import HTTPException


def validate_pagination(limit: int, offset: int) -> None:
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100.")

    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be 0 or greater.")
