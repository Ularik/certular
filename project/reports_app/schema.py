from ninja import Schema
from typing import Optional


class ReportCreateSchema(Schema):
    username: str
    organization: str
    attack_type: str