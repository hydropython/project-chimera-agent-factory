"""Initial migration: create video metadata tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-05
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE creators (
      creator_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      display_name TEXT NOT NULL,
      handle TEXT,
      metadata JSONB,
      created_at TIMESTAMPTZ DEFAULT now()
    );

    CREATE TABLE trends (
      trend_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      name TEXT NOT NULL,
      score DOUBLE PRECISION,
      sources JSONB,
      created_at TIMESTAMPTZ DEFAULT now()
    );

    CREATE TABLE videos (
      video_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      title TEXT,
      description TEXT,
      duration_seconds INTEGER,
      platform TEXT,
      status TEXT,
      trend_id UUID REFERENCES trends(trend_id) ON DELETE SET NULL,
      creator_id UUID REFERENCES creators(creator_id) ON DELETE SET NULL,
      metadata JSONB,
      created_at TIMESTAMPTZ DEFAULT now(),
      updated_at TIMESTAMPTZ DEFAULT now()
    );

    CREATE TABLE content_versions (
      version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      video_id UUID REFERENCES videos(video_id) ON DELETE CASCADE,
      content_blob_ref TEXT,
      checksum TEXT,
      generated_at TIMESTAMPTZ DEFAULT now(),
      model_meta JSONB
    );

    CREATE TABLE reviews (
      review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      version_id UUID REFERENCES content_versions(version_id) ON DELETE CASCADE,
      reviewer_id UUID,
      decision TEXT,
      notes TEXT,
      reviewed_at TIMESTAMPTZ DEFAULT now()
    );

    CREATE TABLE publications (
      publication_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
      version_id UUID REFERENCES content_versions(version_id) ON DELETE CASCADE,
      platform_id TEXT,
      external_id TEXT,
      published_at TIMESTAMPTZ DEFAULT now(),
      status TEXT
    );

    CREATE TABLE video_tags (
      video_id UUID REFERENCES videos(video_id) ON DELETE CASCADE,
      tag TEXT,
      PRIMARY KEY (video_id, tag)
    );

    CREATE INDEX idx_videos_trend ON videos(trend_id);
    CREATE INDEX idx_videos_creator ON videos(creator_id);
    CREATE INDEX idx_trends_score ON trends(score DESC);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS video_tags;
    DROP TABLE IF EXISTS publications;
    DROP TABLE IF EXISTS reviews;
    DROP TABLE IF EXISTS content_versions;
    DROP TABLE IF EXISTS videos;
    DROP TABLE IF EXISTS trends;
    DROP TABLE IF EXISTS creators;
    """)
