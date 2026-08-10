from ninja import Schema


class ReportCreateSchema(Schema):
    username: str | None = None
    organization: str
    name: str

