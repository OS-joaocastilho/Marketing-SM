"""

This code snippet is designed to scrape data from Instagram using the ApifyWrapper from the langchain_community package.
It utilizes the Apify platform's "apify/instagram-scraper" actor to extract specific information from Instagram posts.
"""

from langchain_community.utilities import ApifyWrapper

from marketing_sm.infrastructure.settings import Settings

settings = Settings()
apify = ApifyWrapper(apify_api_token=settings.apify_api_token)


def mapping_fun(item):
    return {
        "caption": item["caption"] or "",
        "alt": item["alt"] or "",
        "commentsCount": item["commentsCount"] or "",
        "hashtags": item["hashtags"] or "",
        "images": item["images"] or "",
        "likesCount": item["likesCount"] or "",
        "date": item["timestamp"] or "",
    }


def scrape_instagram(url):
    loader = apify.call_actor(
        actor_id="apify/instagram-scraper",
        run_input={
            "addParentData": False,
            "directUrls": [url],
            "enhanceUserSearchWithFacebookPage": False,
            "isUserTaggedFeedURL": False,
            "resultsLimit": 200,
            "resultsType": "posts",
            "searchLimit": 1,
            "searchType": "hashtag",
        },
        dataset_mapping_function=mapping_fun,
    )
    data = loader.load()
    return data
