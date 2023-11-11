import strawberry
from strawberry.fastapi import GraphQLRouter

from application.api.graphql.manage.wetbulb import Wetbulb
from application.api.graphql.schema.wetbulb_schema import WetbulbSchema


# # Mutations
# @strawberry.type
# class Mutation:
#     pass


# Queries
@strawberry.type
class Query:
    @strawberry.field
    async def get_wetbulb(self, postal_code: str) -> WetbulbSchema:
        print(postal_code)
        wetbulb_schema = await Wetbulb().get_wetbulb(postal_code)
        return wetbulb_schema


# schema = strawberry.Schema(query=Query, mutation=Mutation)
schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
