"""Project repository."""

from typing import List, Optional
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.errors.database import FailedToCreateEntityError, NotFoundError
from src.models.project import ProjectCreate, ProjectInDb

CREATE_PROJECT_QUERY = """
    INSERT INTO projects (project_id, owner_id, title, description, goal_amount, deadline)
    VALUES (:project_id, :owner_id, :title, :description, :goal_amount, :deadline)
    RETURNING project_id, owner_id, title, description, goal_amount, deadline, created_at, updated_at, is_deleted;
"""

GET_PROJECT_BY_ID_QUERY = """
    SELECT project_id, owner_id, title, description, goal_amount, deadline, created_at, updated_at, is_deleted
    FROM projects
    WHERE project_id = :project_id AND is_deleted = FALSE;
"""

GET_PROJECTS_BY_OWNER_ID_QUERY = """
    SELECT project_id, owner_id, title, description, goal_amount, deadline, created_at, updated_at, is_deleted
    FROM projects
    WHERE owner_id = :owner_id AND is_deleted = FALSE
    ORDER BY created_at DESC;
"""

GET_ALL_PROJECTS_QUERY = """
    SELECT project_id, owner_id, title, description, goal_amount, deadline, created_at, updated_at, is_deleted
    FROM projects
    WHERE is_deleted = FALSE
    ORDER BY created_at DESC;
"""


class ProjectRepository(BaseRepository):
    """Contains logic for all project operations."""

    def __init__(self, db: Database) -> None:
        """Initializes the ProjectRepository with the database instance."""
        super().__init__(db)

    @handle_post_database_exceptions("Project", already_exists_entity="Project title")
    async def create_project(self, *, new_project: ProjectCreate) -> ProjectInDb:
        """Creates a new project."""
        created_project = await self.db.fetch_one(
            query=CREATE_PROJECT_QUERY, values=new_project.model_dump()
        )
        if not created_project:
            raise FailedToCreateEntityError(entity_name="Project.")
        return ProjectInDb(**created_project)  # type: ignore

    @handle_get_database_exceptions("Project")
    async def get_project(self, project_id: Optional[UUID] = None) -> ProjectInDb:
        """Retrieves a project by its ID."""
        search_criteria = {
            "project_id": (GET_PROJECT_BY_ID_QUERY, str(project_id)),
        }

        for field, (query, value) in search_criteria.values():
            if value:
                project_record = await self.db.fetch_one(
                    query=query, values={field: value}
                )
                if project_record:
                    return ProjectInDb(**project_record)  # type: ignore
                else:
                    raise NotFoundError(
                        entity_name="project", entity_identifier=str(project_id)
                    )

        raise ValueError("No search criteria provided.")

    @handle_get_database_exceptions("Project")
    async def get_projects(
        self, *, owner_id: Optional[UUID] = None
    ) -> List[ProjectInDb]:
        """Retrieves all projects owned by a specific user."""
        search_criteria = {
            "owner_id": (GET_PROJECTS_BY_OWNER_ID_QUERY, str(owner_id)),
        }

        for field, (query, value) in search_criteria.values():
            if value:
                projects_records = await self.db.fetch_all(
                    query=query, values={field: value}
                )
                return [ProjectInDb(**project) for project in projects_records]  # type: ignore

        projects_records = await self.db.fetch_all(query=GET_ALL_PROJECTS_QUERY)
        return [ProjectInDb(**project) for project in projects_records]  # type: ignore
