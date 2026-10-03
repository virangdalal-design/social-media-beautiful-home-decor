# 08 — Connections we can reuse from other Bianca projects

Surveyed 2026-10-03 (env var *names* and code only; no secret values were read).

## virangdalal-design/bianca-corporate-sales-agent  (Next.js on Railway)
| Asset there | Reuse here? | How |
|---|---|---|
| **Meta app** (`META_APP_ID`, `META_APP_SECRET`) | **Yes** | Same app can publish Reels. Add the Instagram content-publishing permission to it. |
| `META_PAGE_ID`, `INSTAGRAM_BUSINESS_ACCOUNT_ID` | **Yes** | `INSTAGRAM_BUSINESS_ACCOUNT_ID` = our `IG_USER_ID`. |
| `META_ACCESS_TOKEN` | **Not as is** | Its permissions are `instagram_basic`, `instagram_manage_messages`, `ads_read`, `ads_management` — no `instagram_content_publish`. Generate a **separate** system-user token for Bianca Studio with publish rights (keeps the sales desk's token and blast radius unchanged). |
| **Shopify Admin API** (read-only: `read_products, read_inventory, …`) | **Yes — big win** | biancahome.com runs on Shopify: product names, descriptions, prices, variants, stock and the **original product photos** come straight from the API instead of scraping. Feeds docs/07-PRODUCT-INTAKE.md automatically. Use a separate read-only token (`read_products`, `read_inventory` only). |
| Meta ads insights (`src/meta/ad-insights.ts`) | Later (Phase 3) | Performance write-back for our posted Reels. |
| Railway project | Later (Phase 2) | Host the approval page next to the desk. |
| Anthropic usage | Yes | Can share the org account; use a separate key `bianca-studio` for cost tracking. |

## virangdalal-design/bianca-ai-assistant  (Node, Railway + Supabase BiancaHomeHR)
| Asset there | Reuse here? | How |
|---|---|---|
| Cheap LLM keys: DeepSeek, Kimi (Moonshot), GLM (Z.ai), Groq | **Yes — comparison lane** | Low-cost alternatives for the Strategist/Director text agents; add to `comparison:` in config/models.yaml when keys are added. |
| Multi-provider LLM router pattern (`src/shared/llm.ts`) | Pattern only | Same idea as our config/models.yaml. |
| WhatsApp (Baileys) connector | Later, optional | Phase 2 "approve via WhatsApp" — but prefer the official Cloud API / DoubleTick route the sales agent moved to. |
| Supabase BiancaHomeHR | **No** | HR data — keep separate (same rule the sales agent follows). |

## virangdalal-design/intranet-checking-bot
Not surveyed — attaching it was blocked by session permissions.

## Env vars to add to Bianca Studio (copy values yourself from Railway → the sales-agent service)
| Our variable | Copy from |
|---|---|
| `IG_USER_ID` | `INSTAGRAM_BUSINESS_ACCOUNT_ID` |
| `META_ACCESS_TOKEN` | **new** system-user token with `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`, `business_management` |
| `SHOPIFY_SHOP_DOMAIN` | `SHOPIFY_SHOP_DOMAIN` |
| `SHOPIFY_ADMIN_ACCESS_TOKEN` | same token works (read-only); a separate one is cleaner |
| `SHOPIFY_API_VERSION` | `SHOPIFY_API_VERSION` |
| `DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`, `ZAI_API_KEY`, `GROQ_API_KEY` (optional) | bianca-ai-assistant service |
