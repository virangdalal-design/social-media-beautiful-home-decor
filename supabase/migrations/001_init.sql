create table products (
  id text primary key, name text not null, brand text not null, category text not null,
  brief jsonb not null, created_at timestamptz default now()
);
create table jobs (
  id uuid primary key default gen_random_uuid(), product_id text references products(id),
  status text not null default 'queued',  -- queued|strategy|awaiting_angle_pick|producing|awaiting_approval|approved|rejected|failed
  state jsonb, total_cost_usd numeric default 0, created_at timestamptz default now(), updated_at timestamptz default now()
);
create table angles (
  id text primary key, job_id uuid references jobs(id), type text not null, payload jsonb not null,
  selected boolean default false, performance jsonb  -- hold_rate, ctr, views written back in phase 3
);
create table shots (
  id text primary key, job_id uuid references jobs(id), angle_id text references angles(id),
  "order" int, spec jsonb not null, keyframe_url text, video_url text, model text,
  attempts int default 0, status text default 'pending', cost_usd numeric default 0
);
create table generations (
  id uuid primary key default gen_random_uuid(), job_id uuid, shot_id text, kind text not null, -- keyframe|video|voice|qc
  provider text, model text, params jsonb, output_url text, cost_usd numeric, duration_ms int,
  status text, error text, created_at timestamptz default now()
);
create table qc_reports (
  id uuid primary key default gen_random_uuid(), job_id uuid, shot_id text, stage text, -- keyframe|shot|final
  report jsonb not null, pass boolean, score numeric, created_at timestamptz default now()
);
create table approvals (
  id uuid primary key default gen_random_uuid(), job_id uuid references jobs(id),
  decision text not null, comment text, routed_to text, decided_by text, created_at timestamptz default now()
);
create table benchmark_runs (
  id uuid primary key default gen_random_uuid(), test_shot int, model text, video_url text,
  cost_usd numeric, gen_seconds int, retries int, created_at timestamptz default now()
);
create table benchmark_ratings (
  id uuid primary key default gen_random_uuid(), run_id uuid references benchmark_runs(id),
  rater text, metrics jsonb, total numeric, created_at timestamptz default now()
);
create index on generations(job_id); create index on shots(job_id); create index on jobs(status);
