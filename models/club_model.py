import sqlalchemye

clubs = sqlalchemy.Table(
    "clubs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("soccer_name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("foundation_date", sqlalchemy.String),
    sqlalchemy.Column("amount_titles", sqlalchemy.Integer),
    sqlalchemy.Column("stadium", sqlalchemy.String),
)
