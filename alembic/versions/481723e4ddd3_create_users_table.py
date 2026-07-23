from alembic import op
import sqlalchemy as sa

revision = "481723e4ddd3"
down_revision = None

def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), nullable=False), sa.Column("email", sa.String(255), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=True), sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("email"))

def downgrade() -> None:
    op.drop_table("users")
