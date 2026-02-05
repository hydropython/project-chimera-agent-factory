# Database Schema — Video Metadata (ERD + DDL)

Purpose
- Store canonical metadata for generated/published video content, link content to agents and trends, and track publication/review history.

ERD (conceptual)
- `videos` (pk: video_id)
- `creators` (pk: creator_id)
- `trends` (pk: trend_id)
- `video_tags` (video_id, tag) — many-to-many
- `content_versions` (pk: version_id) — multiple content drafts/variants per video
- `reviews` (pk: review_id) — human safety reviews
- `publications` (pk: publication_id) — records of publishing to platforms

PlantUML (textual)
```
@startuml
entity videos {
  *video_id : uuid
  --
  title : varchar
  description : text
  duration_seconds : int
  platform : varchar
  status : varchar
  trend_id : uuid
  creator_id : uuid
  created_at : timestamptz
  updated_at : timestamptz
}

entity creators {
  *creator_id : uuid
  display_name : varchar
  handle : varchar
  metadata : jsonb
}

entity trends {
  *trend_id : uuid
  name : varchar
  score : float
  sources : jsonb
}

entity content_versions {
  *version_id : uuid
  video_id : uuid
  content_blob_ref : varchar
  checksum : varchar
  generated_at : timestamptz
  model_meta : jsonb
}

entity reviews {
  *review_id : uuid
  version_id : uuid
  reviewer_id : uuid
  decision : varchar
  notes : text
  reviewed_at : timestamptz
}

entity publications {
  *publication_id : uuid
  version_id : uuid
  platform_id : varchar
  external_id : varchar
  published_at : timestamptz
  status : varchar
}

videos }|--|| creators
videos }|--|| trends
videos ||--o{ content_versions
content_versions ||--o{ reviews
content_versions ||--o{ publications
@enduml
```

SQL DDL (Postgres-flavored) — primary tables

```sql
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

-- Indexes
CREATE INDEX idx_videos_trend ON videos(trend_id);
CREATE INDEX idx_videos_creator ON videos(creator_id);
CREATE INDEX idx_trends_score ON trends(score DESC);
```

Notes and Recommendations
- Use `jsonb` for flexible metadata but store frequently queried fields (e.g., `platform`, `status`, `duration_seconds`) as first-class columns for indexing.
- Retention: consider TTL policies for raw assets; keep metadata/audit logs longer for traceability.
- Backups: snapshot DB nightly; export immutable audit logs to object storage.
