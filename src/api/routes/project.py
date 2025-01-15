"""Project routes."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies.auth import get_current_user
from src.api.dependencies.database import get_repository
from src.db.repositories.contribution import ContributionRepository
from src.db.repositories.project import ProjectRepository
from src.models.contribution import (
    ContributionCreate,
    ContributionInDb,
    ContributionPublic,
)
from src.models.project import ProjectCreate, ProjectInDb, ProjectPublic
from src.models.user import UserInDb

project_router = APIRouter()


@project_router.post(
    "",
    response_model=ProjectPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    new_project: ProjectCreate,
    project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
    user: UserInDb = Depends(get_current_user),
) -> ProjectInDb:
    """Register a new project."""
    if user.user_id != new_project.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create projects for yourself.",
        )
    return await project_repo.create_project(new_project=new_project)


@project_router.get(
    "",
    response_model=list[ProjectPublic],
    status_code=status.HTTP_200_OK,
)
async def get_projects(
    owner_id: Optional[UUID] = Query(None, description="The owner's ID"),
    project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
) -> list[ProjectInDb]:
    """Get the current user."""
    return await project_repo.get_projects(owner_id=owner_id)


@project_router.get(
    "/{project_id}",
    response_model=ProjectPublic,
    status_code=status.HTTP_200_OK,
)
async def get_project_by_id(
    project_id: UUID,
    project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
) -> ProjectInDb:
    """Get the current user."""
    return await project_repo.get_project(project_id=project_id)


@project_router.post(
    "{project_id}/contribute",
    response_model=ContributionPublic,
    status_code=status.HTTP_201_CREATED,
)
async def create_contribution(
    project_id: UUID,
    new_contribution: ContributionCreate,
    contribution_repo: ContributionRepository = Depends(
        get_repository(ContributionRepository)
    ),
    project_repo: ProjectRepository = Depends(get_repository(ProjectRepository)),
    user: UserInDb = Depends(get_current_user),
) -> ContributionInDb:
    """Register a new contribution."""
    project = await project_repo.get_project(project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    if project.deadline < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project deadline has passed.",
        )
    return await contribution_repo.create_contribution(
        project_id=project_id, new_contribution=new_contribution
    )
