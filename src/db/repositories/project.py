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

GET_PROJECT_CONTRIBUTORS_QUERY = """
    SELECT
        u.username,
    FROM contributions c
    INNER JOIN users u ON c.contributor_id = u.user_id
    WHERE c.project_id = :project_id
    AND c.is_deleted = FALSE
    ORDER BY c.created_at DESC;
"""

GET_PROJECT_QUERY = """
    WITH project_data AS (
        SELECT
            p.project_id,
            p.owner_id,
            p.title,
            p.description,
            p.goal_amount,
            p.deadline,
            p.created_at,
            p.updated_at,
            COUNT(DISTINCT c.contributor_id) as contribution_count,
            ARRAY_AGG(DISTINCT u.username) FILTER (WHERE u.username IS NOT NULL) as contributor_usernames
        FROM projects p
        LEFT JOIN contributions c ON p.project_id = c.project_id AND c.is_deleted = FALSE
        LEFT JOIN users u ON c.contributor_id = u.user_id
        WHERE p.is_deleted = FALSE
        {where_clause}
        GROUP BY 
            p.project_id,
            p.owner_id,
            p.title,
            p.description,
            p.goal_amount,
            p.deadline,
            p.created_at,
            p.updated_at
        ORDER BY p.created_at DESC
    )
    SELECT *
    FROM project_data
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
    async def get_single_project_efficient(self, project_id: UUID) -> ProjectInDb:
        """Get a project."""
        projects = await self.get_projects_efficient(project_id=project_id)
        if not projects:
            raise NotFoundError(
                entity_name="Project", entity_identifier=str(project_id)
            )
        return projects[0]

    @handle_get_database_exceptions("Project")
    async def get_owner_projects_efficient(self, owner_id: UUID) -> List[ProjectInDb]:
        """Get all of owners project."""
        return await self.get_projects_efficient(owner_id=owner_id)

    @handle_get_database_exceptions("Project")
    async def get_all_projects_efficient(self) -> List[ProjectInDb]:
        """Get all projects."""
        return await self.get_projects_efficient()

    async def get_projects_efficient(
        self, project_id: Optional[UUID] = None, owner_id: Optional[UUID] = None
    ) -> List[ProjectInDb]:
        """General get projects."""
        where_conditions = []
        values = {}

        if project_id:
            where_conditions.append("p.project_id = :project_id")
            values["project_id"] = str(project_id)

        if owner_id:
            where_conditions.append("p.owner_id = :owner_id")
            values["owner_id"] = str(owner_id)

        where_clause = (
            f"AND {' AND '.join(where_conditions)}" if where_conditions else ""
        )

        query = GET_PROJECT_QUERY.format(where_clause=where_clause)
        records = await self.db.fetch_all(query=query, values=values)

        projects = []
        for record in records:
            project_data = dict(record)

            usernames = project_data.get("contributor_usernames")
            if usernames is None:
                project_data["contributor_usernames"] = []
            elif isinstance(usernames, str):
                clean_usernames = usernames.strip("{}").split(",")
                project_data["contributor_usernames"] = [
                    u for u in clean_usernames if u
                ]

            projects.append(ProjectInDb(**project_data))

        return projects
