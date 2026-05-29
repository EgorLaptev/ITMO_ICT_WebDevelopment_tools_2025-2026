from fastapi import FastAPI

from app.config import settings
from app.database import init_db
from app.routers import auth, evaluations, hackathons, submissions, tasks, teams, users, parser_queue

app = FastAPI(title="Hackathon Management System")

app.include_router(auth.router)
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(hackathons.router, prefix="/hackathons", tags=["hackathons"])
app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(submissions.router, prefix="/submissions", tags=["submissions"])
app.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])
app.include_router(parser_queue.router, prefix="/parser", tags=["parser queue"])

@app.on_event("startup")
async def on_startup() -> None:
    if settings.create_tables_on_startup:
        await init_db()