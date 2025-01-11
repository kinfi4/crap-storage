import strawberry
from strawberry.fastapi import GraphQLRouter

from .schema import Query
from .context import get_context


router = GraphQLRouter(
    schema=strawberry.Schema(Query),
    context_getter=get_context,
)
