---
name: facebook-marketing
description: >
  Post content to a Facebook Page, like posts and comments, reply to comments,
  and fetch page activity using the Meta Graph API. Use this skill when the agent
  needs to publish Facebook posts, engage with audience comments, or run automated
  social media marketing for a Facebook Page.
  Requires FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN in the environment.
version: 1.0.0
license: MIT
platforms:
  - linux
  - macos
  - windows
required_environment_variables:
  - name: FB_PAGE_ID
    description: The numeric ID of your Facebook Page
  - name: FB_PAGE_ACCESS_TOKEN
    description: >
      Long-lived Page Access Token with permissions:
      pages_manage_posts, pages_read_engagement, pages_manage_engagement
metadata:
  category: social-media
  author: hermes-facebook-skill
---

# Facebook Marketing Skill

Connects Hermes to a Facebook Page via the Meta Graph API. Provides autonomous
posting, comment engagement, and rule-based reply logic for business Pages.

## When to Use

- The user asks you to post something on Facebook
- The user wants to engage with comments on their Page
- You are running a scheduled daily marketing loop
- You need to fetch recent posts or comments for analysis

## Procedure

### Setup (one-time)

1. Ensure `FB_PAGE_ID` and `FB_PAGE_ACCESS_TOKEN` are set in the environment.
   The connector loads them automatically from `.env` if present.
2. Install dependencies: `pip install requests python-dotenv`

### Posting content

```python
from skills.facebook.scripts.connector import post_to_facebook

post_id = post_to_facebook(
    text="Your post text here.",
    link="https://yourbroker.ly/product",   # optional
    image_url="https://cdn.example.com/image.jpg",  # optional
    publish=True,  # False = save as draft
)
```

### Engaging with comments

```python
from skills.facebook.scripts.connector import (
    get_page_comments,
    like_facebook_post,
    reply_to_facebook_comment,
)

comments = get_page_comments(post_id)
for comment in comments:
    like_facebook_post(comment["id"])
    # classify comment["message"] and call reply_to_facebook_comment if appropriate
```

### Reply decision logic

Classify the comment text before replying. See
`references/reply-templates.md` for bilingual (EN/AR) reply templates and
the full classification ruleset.

**Rule summary:**

| Comment type | Action |
|---|---|
| Price / quote request | Auto-reply with DM CTA |
| Compliment / positive | Auto-reply with thank-you |
| Claim / complaint / problem | Flag for human review, do NOT auto-reply |
| General question | Auto-reply with contact prompt |

### Flagging sensitive comments

Do not auto-reply when any of these keywords appear:
`claim, problem, issue, complaint, unhappy, مشكلة, شكوى, تعويض`

Instead, output:
```
[REVIEW NEEDED] comment_id=<id> message="<text>"
```
and skip the `reply_to_facebook_comment` call.

## Available Functions

| Function | Description |
|---|---|
| `post_to_facebook(text, image_url, link, publish)` | Publish or draft a post |
| `like_facebook_post(post_id)` | Like a post or comment as the Page |
| `comment_on_facebook_post(post_id, text)` | Add a top-level comment |
| `reply_to_facebook_comment(comment_id, text)` | Reply to a comment |
| `get_page_comments(post_id, limit)` | Fetch comments on a post |
| `get_recent_posts(limit)` | Fetch the Page's recent feed |

## Daily Automation Loop (SOUL / cron prompt)

```
Every day at 09:00:
1. Generate 1–3 Facebook posts aligned with the content plan.
2. Call post_to_facebook() for each approved post.
3. Fetch comments on all posts from the last 7 days.
4. For each comment:
   a. Call like_facebook_post(comment_id).
   b. Classify the comment text.
   c. If safe to reply, call reply_to_facebook_comment(comment_id, reply).
   d. If sensitive, print REVIEW NEEDED and stop.
```

## Pitfalls

- **Tokens expire**: Long-lived tokens last ~60 days. Renew before expiry.
- **Rate limits**: Do not loop over hundreds of objects without a `time.sleep(0.5)` between calls.
- **Draft vs publish**: `publish=False` creates an unpublished post — it will not appear on the Page until manually published.
- **Likes on comments**: `like_facebook_post` works on both post IDs and comment IDs.

## Verification

After running `post_to_facebook`, the function prints:
```
[facebook] Post published successfully. ID: <post_id>
```
If you see `[facebook] Failed to post:` check that your token has not expired
and that the `FB_PAGE_ID` is the numeric page ID, not the page username.
