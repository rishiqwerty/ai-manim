import uuid
from fastapi import Request

async def anonymous_tracking_middleware(request: Request, call_next):
    user_id = request.cookies.get("anonymous_id")
    response = await call_next(request)
    
    if not user_id:
        new_id = str(uuid.uuid4())
        response.set_cookie(key="anonymous_id", value=new_id, httponly=True)
        print(f"Assigned new anonymous_id: {new_id}")
    else:
        print(f"Returning user with anonymous_id: {user_id}")
    
    return response
