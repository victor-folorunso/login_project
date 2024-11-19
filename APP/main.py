from fastapi import FastAPI
from APP.routes.signup_router import SIGNUP_ROUTER
from APP.routes.rootpage_router import ROOTPAGE_ROUTER
from APP.routes.login_router import LOGIN_ROUTER
from APP.routes.homepage_router import HOMEPAGE_ROUTER
from APP.admin_routes.showusers_router import SHOWUSERS_ROUTER
from APP.admin_routes.deleteall_users_router import DELETEALL_USERS_ROUTER
from APP.routes.verify_otp import VERIFY_OTP_ROUTER


app = FastAPI(
    debug = False,
    title="login project API",
    version="0.0.1",
    description="This is a full login / sign up API with advanced features and security without sacrificing code simplicity.\nIt is built using fastapi at its core,uvicorn, mysql, and python prisma ORM.\n\nIt is supposed to be a reusable code and serves as part of larger projects.",
)

all_routes = [
    SIGNUP_ROUTER,
    ROOTPAGE_ROUTER,
    LOGIN_ROUTER,
    HOMEPAGE_ROUTER,
    VERIFY_OTP_ROUTER,
    SHOWUSERS_ROUTER,
    DELETEALL_USERS_ROUTER,
]

for route in all_routes:
    app.include_router(route)
