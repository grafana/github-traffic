from github import Github
from decouple import config
from prometheus_client import start_http_server, Gauge
from decouple import config
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from prometheus_client import start_http_server, Gauge

ORG_NAME = config("ORG_NAME")
REPO_TYPE = config("REPO_TYPE", default="public")
REPO_NAME_CONTAINS = config("REPO_NAME_CONTAINS", default="")
CRONTAB_SCHEDULE = config("CRONTAB_SCHEDULE", default="0 * * * *")
GITHUB_TOKEN = config('GITHUB_TOKEN')

github = Github(GITHUB_TOKEN)

gh_traffic_views = Gauge(
    "github_traffic_views",
    "Number of views",
    ["repository"],
)

gh_traffic_unique_views = Gauge(
    "github_traffic_unique_views",
    "Number of unique views",
    ["repository"],
)

gh_traffic_clones = Gauge(
    "github_traffic_clones",
    "Number of clones",
    ["repository"],
)

gh_traffic_unique_clones = Gauge(
    "github_traffic_unique_clones",
    "Number of unique views",
    ["repository"],
)

gh_traffic_stars = Gauge(
    "github_traffic_stars",
    "Number of stars",
    ["repository"],
)

gh_traffic_api_requests_limit = Gauge(
    "github_traffic_api_requests_limit",
    "Requests limit from Github API limits",
)

gh_traffic_api_requests_remaining = Gauge(
    "github_traffic_api_requests_remaining",
    "Requests remaining from Github API limits",
)

def job_function():
    api_limits = github.get_rate_limit().core
    gh_traffic_api_requests_limit.set(api_limits.limit)
    gh_traffic_api_requests_remaining.set(api_limits.remaining)

    repositories = github.get_organization(ORG_NAME).get_repos(type=REPO_TYPE)
    for repo in repositories:
        if REPO_NAME_CONTAINS in repo.name:
            repo_name = repo.name
            print(repo.name)

            try:
                # Views stats
                data_views = repo.get_views_traffic(per="day")
                print(data_views["views"][-1].count)
                gh_traffic_views.labels(repo_name).set(data_views["views"][-1].count)
                print(data_views["views"][-1].uniques)
                gh_traffic_unique_views.labels(repo_name).set(data_views["views"][-1].uniques)

                # Clones stats
                data_clones = repo.get_clones_traffic(per="day")
                print(data_clones["clones"][-1].count)
                gh_traffic_clones.labels(repo_name).set(data_clones["clones"][-1].count)
                print(data_clones["clones"][-1].uniques)
                gh_traffic_unique_clones.labels(repo_name).set(data_clones["clones"][-1].uniques)

                # Star stats
                gh_traffic_stars.labels(repo_name).set(repo.stargazers_count)
            except Exception as e:
                print(f"Failed to extract stats on {repo_name}: {e}")


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8001)
    # Schedule run the job on startup.
    job_function()
    # Start scheduler
    sched = BlockingScheduler()
    sched.add_job(job_function, CronTrigger.from_crontab(CRONTAB_SCHEDULE))
    sched.start()
