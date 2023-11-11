from fastapi import FastAPI

from application.api.graphql.router import graphql_app
# from application.api.ui import admin

app = FastAPI()

# orgins = [
#     'https://www.whatiswetbulb.com'
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

# GraphQL router
app.include_router(graphql_app, prefix='/graphql', tags=['GraphQL'])

# UI router
# app.include_router(admin.router)
