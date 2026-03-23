# hermes-facebook-skill

A plug-and-play skill for [Hermes Agent by Nous Research](https://github.com/NousResearch/hermes-agent)
that connects your agent to a Facebook Page via the Meta Graph API.

Designed for insurance and reinsurance brokers — and any business — that want
autonomous, rule-based Facebook marketing without a dedicated social media team.

---

## What this skill does

- Publishes posts (text, image, link) to your Facebook Page
- Likes posts and comments automatically as the Page
- Posts comments and replies to comments with rule-based, bilingual responses
- Fetches recent posts and comments for agent processing
- Flags sensitive comments (claims, complaints) for human review before any reply is sent

---

## Repo structure

```
hermes-facebook-skill/
├── skills/
│   └── facebook/               <- copy this entire folder to ~/.hermes/skills/facebook/
│       ├── SKILL.md            <- agentskills.io skill definition (loaded by Hermes)
│       ├── scripts/
│       │   └── connector.py   <- Meta Graph API connector
│       └── references/
│           └── reply-templates.md  <- bilingual EN/AR reply templates
├── .env.example                <- template for your credentials
├── .gitignore
├── README.md
└── LICENSE
```

---

## Prerequisites

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) installed
- Python 3.9+
- `pip install requests python-dotenv`
- A Meta Developer App with a Facebook Page linked
- A long-lived Page Access Token with these permissions:
  - `pages_manage_posts`
  - `pages_read_engagement`
  - `pages_manage_engagement`

To get a long-lived token, follow Meta's guide:
https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived

---

## Installation

**Step 1.** Clone or download this repo.

**Step 2.** Copy the skill folder into your Hermes skills directory:

```bash
cp -r skills/facebook/ ~/.hermes/skills/facebook/
```

**Step 3.** Copy `.env.example` to `.env` in the same location and fill in your credentials:

```bash
cp .env.example ~/.hermes/skills/facebook/.env
```

Open the file and replace every placeholder with your real values.

**Step 4.** Install Python dependencies:

```bash
pip install requests python-dotenv
```

**Step 5.** Test the connector directly:

```bash
python ~/.hermes/skills/facebook/scripts/connector.py
```

If everything is configured correctly, you will see a test post appear on your Facebook Page.

**Step 6.** Restart Hermes (or send `/reset`) so it picks up the new skill:

```bash
hermes skills config   # optional: verify facebook-marketing is listed and enabled
```

---

## How Hermes activates this skill

Hermes reads the `SKILL.md` frontmatter at startup. The `description` field is
used as the activation trigger. When you give Hermes a task like:

> "Post about our motor insurance offer on Facebook"
> "Check for new comments on our page and reply to them"
> "Run the daily Facebook marketing loop"

...Hermes will load the full `SKILL.md` body, see the procedure, and call
`connector.py` functions accordingly.

---

## Getting started — Python snippet

You can also call the connector directly from your own Python scripts or
from a Hermes plugin:

```python
import sys
sys.path.insert(0, "~/.hermes/skills/facebook/scripts")

from connector import (
    post_to_facebook,
    like_facebook_post,
    reply_to_facebook_comment,
    get_page_comments,
    get_recent_posts,
)

# The connector loads .env automatically — no manual load_dotenv() needed.

# 1. Publish a post
post_id = post_to_facebook(
    text="Protect your business with our commercial insurance plans. Contact us today.",
    link="https://yourbroker.ly/commercial"
)

# 2. Fetch and process comments
comments = get_page_comments(post_id)

SENSITIVE = ["claim", "problem", "issue", "complaint", "مشكلة", "شكوى", "تعويض"]
PRICE     = ["price", "cost", "quote", "how much", "سعر", "كم", "تكلفة"]
POSITIVE  = ["thank", "great", "excellent", "شكر", "ممتاز", "رائع"]

for comment in comments:
    cid     = comment["id"]
    message = comment["message"].lower()

    # Always like every comment
    like_facebook_post(cid)

    if any(w in message for w in SENSITIVE):
        print(f"[REVIEW NEEDED] comment_id={cid} message=\"{comment['message']}\"")

    elif any(w in message for w in PRICE):
        reply_to_facebook_comment(
            cid,
            "Thank you for your interest! Please send us a direct message with "
            "your details and we will prepare a tailored quote for you."
        )

    elif any(w in message for w in POSITIVE):
        reply_to_facebook_comment(
            cid,
            "We truly appreciate your kind words! Visit our website to learn more."
        )

    else:
        reply_to_facebook_comment(
            cid,
            "Thank you for reaching out! Please message us directly for more information."
        )
```

---

## Agent persona design

### Daily automation loop

Tell Hermes to run these tasks every day (natural language cron syntax):

```
Every day at 09:00:
  - Generate 1-3 Facebook posts from the monthly content plan and publish them.
  - Fetch all comments from the last 7 days on page posts.
  - For each comment: like it, classify it, and reply if appropriate.
  - Flag sensitive comments for human review without auto-replying.
```

### SOUL / system prompt template

Add this block to your Hermes SOUL file or agent system prompt:

```
You are a Facebook marketing agent for [BUSINESS_NAME], an insurance and
reinsurance broker in [COUNTRY].

Your tone is professional, warm, and bilingual (English and Arabic).
You have access to the facebook-marketing skill.

When you see a new comment on a business post, follow this logic:

  PRICE or QUOTE request
  (keywords: price, cost, quote, how much, سعر, كم, تكلفة)
  → Reply: "Thank you for your interest! Please send us a direct message with
    your details and we will prepare a tailored quote for you."
  → Call: reply_to_facebook_comment(comment_id, reply_text)

  COMPLIMENT or POSITIVE feedback
  (keywords: thank, great, excellent, شكر, ممتاز, رائع)
  → Reply: "We truly appreciate your kind words! Visit [WEBSITE] to learn more."
  → Call: reply_to_facebook_comment(comment_id, reply_text)

  CLAIM, PROBLEM, or COMPLAINT
  (keywords: claim, problem, complaint, مشكلة, شكوى, تعويض)
  → DO NOT auto-reply.
  → Output: "[REVIEW NEEDED] comment_id=<id> message=<text>"

  GENERAL QUESTION or OTHER
  → Reply: "Thank you! For more information please message us or call [PHONE]."
  → Call: reply_to_facebook_comment(comment_id, reply_text)

Always call like_facebook_post(comment_id) for every comment before deciding on a reply.

For daily posts, generate content on these topics:
motor insurance, health insurance, marine cargo, fire and property,
life insurance, reinsurance. Keep posts 2-4 sentences with a call to action
and relevant Arabic and English hashtags.
```

### Automation settings reference

| Feature | Recommended setting | Rationale |
|---|---|---|
| Post publishing | `AUTO_PUBLISH_POSTS=true` | Safe for scheduled content |
| Liking comments | `AUTO_LIKE_COMMENTS=true` | Zero risk, positive signal |
| Replies to questions | `AUTO_REPLY_COMMENTS=true` | Rule-based, low risk |
| Replies to complaints | Always manual | Never auto-reply to unhappy customers |

---

## Security and automation guidelines

- **Never commit `.env` to GitHub.** The `.gitignore` in this repo already excludes it.
  Your Page Access Token gives full posting access to your business page.
- **Rate limits**: Meta enforces per-app and per-page API limits. Add a
  `time.sleep(0.3)` between calls when processing large batches of comments.
- **Avoid repetitive replies**: The rule-based classifier above ensures each reply
  is contextually relevant. Do not send the same generic message to every comment.
- **Token expiry**: Long-lived tokens last approximately 60 days. Set a calendar
  reminder to refresh `FB_PAGE_ACCESS_TOKEN` before it expires.
- **Permission hygiene**: Only request the three permissions listed in Prerequisites.
  Revoke any extras from your Meta App dashboard.

---

## License

MIT License. See `LICENSE`.
