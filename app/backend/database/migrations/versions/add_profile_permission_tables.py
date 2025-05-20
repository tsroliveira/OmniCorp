"""add profile permission tables

Revision ID: add_profile_permission_tables
Revises: 
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_profile_permission_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Criar tabela de perfis
    op.create_table(
        'profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Criar tabela de permissões
    op.create_table(
        'permission',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Criar tabela de relacionamento entre perfis e permissões
    op.create_table(
        'profile_permissions',
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('permission_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id'], ),
        sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
        sa.PrimaryKeyConstraint('profile_id', 'permission_id')
    )

    # Adicionar coluna profile_id na tabela de usuários
    op.add_column('user', sa.Column('profile_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_user_profile',
        'user', 'profile',
        ['profile_id'], ['id']
    )


def downgrade():
    # Remover coluna profile_id da tabela de usuários
    op.drop_constraint('fk_user_profile', 'user', type_='foreignkey')
    op.drop_column('user', 'profile_id')

    # Remover tabelas
    op.drop_table('profile_permissions')
    op.drop_table('permission')
    op.drop_table('profile') 