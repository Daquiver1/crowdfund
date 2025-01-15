"""Contribution repository."""

from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import handle_post_database_exceptions
from src.errors.database import FailedToCreateEntityError
from src.models.contribution import ContributionCreate, ContributionInDb

CREATE_CONTRIBUTION_QUERY = """
    INSERT INTO contributions (id, project_id, contributor_id, amount)
    VALUES (:id, :project_id, :contributor_id, :amount)
    RETURNING id, project_id, contributor_id, amount, created_at, updated_at, is_deleted;
"""

GET_CONTRIBUTION_BY_ID_QUERY = """
    SELECT id, project_id, contributor_id, amount, created_at, updated_at, is_deleted
    FROM contributions
    WHERE id = :id AND is_deleted = FALSE;
"""

GET_CONTRIBUTIONS_BY_PROJECT_ID_QUERY = """
    SELECT id, project_id, contributor_id, amount, created_at, updated_at, is_deleted
    FROM contributions
    WHERE project_id = :project_id AND is_deleted = FALSE
    ORDER BY created_at DESC;
"""

GET_CONTRIBUTIONS_BY_CONTRIBUTOR_ID_QUERY = """
    SELECT id, project_id, contributor_id, amount, created_at, updated_at, is_deleted
    FROM contributions
    WHERE contributor_id = :contributor_id AND is_deleted = FALSE
    ORDER BY created_at DESC;
"""


class ContributionRepository(BaseRepository):
    """Contains logic for all contribution operations."""

    def __init__(self, db: Database) -> None:
        """Initializes the ContributionRepository with the database instance."""
        super().__init__(db)

    @handle_post_database_exceptions(
        "Contribution", already_exists_entity="Contribution ID"
    )
    async def create_contribution(
        self, *, project_id: UUID, new_contribution: ContributionCreate
    ) -> ContributionInDb:
        """Creates a new contribution."""
        contribution = new_contribution.model_dump()
        contribution["project_id"] = project_id

        created_contribution = await self.db.fetch_one(
            query=CREATE_CONTRIBUTION_QUERY, values=contribution
        )
        if not created_contribution:
            raise FailedToCreateEntityError(entity_name="Contribution.")
        return ContributionInDb(**created_contribution)  # type: ignore
