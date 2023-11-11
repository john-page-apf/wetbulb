import strawberry
import decimal


@strawberry.type
class WetbulbSchema:
    wetbulb: decimal.Decimal = 0.0
