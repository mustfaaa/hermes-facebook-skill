import os
import requests

# Load .env automatically so users can run this script directly
# without manually exporting environment variables.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; assume env vars are already set

GRAPH_API_BASE = "https://graph.facebook.com/v19.0"


def _page_id():
    return os.getenv("FB_PAGE_ID")


def _token():
    return os.getenv("FB_PAGE_ACCESS_TOKEN")


def _check_env():
    if not _page_id() or not _token():
        raise EnvironmentError(
            "FB_PAGE_ID and FB_PAGE_ACCESS_TOKEN must be set.\n"
            "Copy .env.example to .env and fill in your credentials."
        )


def post_to_facebook(text, image_url=None, link=None, publish=True):
    """
    Publish a post to the Facebook Page.
    Returns the new post ID on success, None on failure.
    """
    _check_env()

    if image_url:
        url = f"{GRAPH_API_BASE}/{_page_id()}/photos"
        payload = {
            "caption": text,
            "url": image_url,
            "published": publish,
            "access_token": _token(),
        }
    else:
        url = f"{GRAPH_API_BASE}/{_page_id()}/feed"
        payload = {
            "message": text,
            "published": publish,
            "access_token": _token(),
        }
        if link:
            payload["link"] = link

    response = requests.post(url, data=payload)
    data = response.json()

    if response.ok and ("id" in data or "post_id" in data):
        post_id = data.get("id") or data.get("post_id")
        print(f"[facebook] Post published. ID: {post_id}")
        return post_id

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to post: {error}")
    return None


def like_facebook_post(post_id):
    """
    Like a post or comment as the Page.
    Returns True on success, False on failure.
    """
    _check_env()

    url = f"{GRAPH_API_BASE}/{post_id}/likes"
    response = requests.post(url, data={"access_token": _token()})
    data = response.json()

    if response.ok and data.get("success"):
        print(f"[facebook] Liked: {post_id}")
        return True

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to like {post_id}: {error}")
    return False


def comment_on_facebook_post(post_id, text):
    """
    Post a top-level comment on a Facebook post.
    Returns the new comment ID on success, None on failure.
    """
    _check_env()

    url = f"{GRAPH_API_BASE}/{post_id}/comments"
    payload = {"message": text, "access_token": _token()}

    response = requests.post(url, data=payload)
    data = response.json()

    if response.ok and "id" in data:
        print(f"[facebook] Comment posted on {post_id}. ID: {data['id']}")
        return data["id"]

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to comment on {post_id}: {error}")
    return None


def reply_to_facebook_comment(comment_id, text):
    """
    Reply to an existing comment.
    Returns the new reply ID on success, None on failure.
    """
    _check_env()

    url = f"{GRAPH_API_BASE}/{comment_id}/comments"
    payload = {"message": text, "access_token": _token()}

    response = requests.post(url, data=payload)
    data = response.json()

    if response.ok and "id" in data:
        print(f"[facebook] Replied to {comment_id}. Reply ID: {data['id']}")
        return data["id"]

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to reply to {comment_id}: {error}")
    return None


def get_page_comments(post_id, limit=25):
    """
    Fetch recent comments on a post.
    Returns a list of dicts with keys: id, message, from, created_time.
    """
    _check_env()

    url = f"{GRAPH_API_BASE}/{post_id}/comments"
    params = {
        "fields": "id,message,from,created_time",
        "limit": limit,
        "access_token": _token(),
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.ok and "data" in data:
        comments = data["data"]
        print(f"[facebook] Fetched {len(comments)} comments from {post_id}.")
        return comments

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to fetch comments for {post_id}: {error}")
    return []


def get_recent_posts(limit=10):
    """
    Fetch the Page's recent posts.
    Returns a list of dicts with keys: id, message, created_time.
    """
    _check_env()

    url = f"{GRAPH_API_BASE}/{_page_id()}/feed"
    params = {
        "fields": "id,message,created_time",
        "limit": limit,
        "access_token": _token(),
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.ok and "data" in data:
        posts = data["data"]
        print(f"[facebook] Fetched {len(posts)} recent posts.")
        return posts

    error = data.get("error", {}).get("message", response.text)
    print(f"[facebook] Failed to fetch posts: {error}")
    return []


if __name__ == "__main__":
    print("Running Facebook connector test...")
    _check_env()

    test_text = (
        "This is a test post from the Hermes Facebook skill. "
        "If you can see this, the connector is working correctly."
    )

    post_id = post_to_facebook(text=test_text)
    if post_id:
        print(f"Test succeeded. Post ID: {post_id}")
    else:
        print("Test failed. Check your credentials and token permissions.")
