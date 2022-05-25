from wikibase_api import Wikibase


class Wikibaseapi:
    def __init__(self, url, wb):
        url = "http://156.35.98.119/w/api.php"

        credentials = {
            "bot_username": "Admin",
            "bot_password": "bot@9eomjq89fmimaa11t2gilnkh64ed398p",
        }
        wb = Wikibase(
            api_url='http://156.35.98.119/w/api.php',
            oauth_credentials=None,
            login_credentials=credentials,
            is_bot=True
        )

    def insert(self, content):
        r = self.wb.entity.add("item")
        # content = {"labels": {"en": {"language": "en", "value": "Updated label"}}}
        updated = self.wb.entity.update(r["entity"]["id"], content=content)
        print(updated)
