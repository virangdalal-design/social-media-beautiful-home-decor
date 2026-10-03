-- Storage buckets: public for final renders (Instagram fetches by URL), private for everything else.
insert into storage.buckets (id, name, public, file_size_limit)
values
  ('bianca-studio', 'bianca-studio', true, 104857600),           -- 100 MB, Instagram API limit
  ('bianca-studio-private', 'bianca-studio-private', false, 5368709120)  -- 5 GB, 4K masters
on conflict (id) do nothing;

-- Lock every table: only the service role (server-side pipeline) reads or writes.
-- No anon/authenticated policies are created, so the public API key sees nothing.
alter table products enable row level security;
alter table jobs enable row level security;
alter table angles enable row level security;
alter table shots enable row level security;
alter table generations enable row level security;
alter table qc_reports enable row level security;
alter table approvals enable row level security;
alter table benchmark_runs enable row level security;
alter table benchmark_ratings enable row level security;
