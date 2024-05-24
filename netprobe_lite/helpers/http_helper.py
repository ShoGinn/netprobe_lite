import requests


class CallHome:  # Call home http functions
    def __init__(self) -> None:
        pass

    def post_stats(self, url: str | bytes, stats: str | None) -> tuple[int, bytes]:
        headers = {"Content-Type": "application/json"}

        request = requests.post(url, data=stats, headers=headers)

        return (request.status_code, request.content)
