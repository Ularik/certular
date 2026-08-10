from ninja import Schema
from typing import Optional


class ReportCreateSchema(Schema):
    username: str | None = None
    organization: str
    attack_type: str