import datetime
from dateutil.relativedelta import relativedelta
from github import Github

# token = 'a0f8dc4c9af976ed9e552f637ba1c25c326e24a2'


def __init__(self, token, org, repo):
    self.token = token
    self.org = org
    self.repo = repo
    self.full_repo_name = org + '/' + repo


def get_month_before(before, basepoint=datetime.datetime.now()):
    """
    :param self
    :param before: int
    :param basepoint: datetime.datetime
    :rtype: :class: datetime
    """
    return basepoint - relativedelta(months=+before)


def get_day_before(before, basepoint=datetime.datetime.now()):
    """
    :param self
    :param before: int
    :param basepoint: datetime.datetime
    :rtype: :class: datetime
    """
    return basepoint - relativedelta(days=+before)


def get_stargazers(token, repository='bitcoin/bitcoin'):
    """
    :param token
    :param repo: full name of github repo
    :rtype: :
    """
    g = Github(token)
    repo = g.get_repo(repository)
    stargazers = repo.get_stargazers_with_dates()
    for people in stargazers:
        print(people.starred_at)
        print(people.user)


def get_commits(token, repository='bitcoin/bitcoin'):
    """
    :param token
    :param repo: full name of github repo
    :rtype: :
    """
    g = Github(token)
    repo = g.get_repo(repository)
    stargazers = repo.get_stargazers_with_dates()
    for people in stargazers:
        print(people.starred_at)
        print(people.user)


def get_commits_count(token, repository):
    """
    repository='bitcoin/bitcoin'
    # https://api.github.com/repos/bitcoin/bitcoin/commits
    :param token
    :param repository: full name of github repo
    :rtype: :
    """
    g = Github(token)
    repo = g.get_repo(repository)

    mm = repo.get_commits('master', '', get_day_before(7))
    cnt = 0
    committer_set = set()
    sha_set = set()
    try:
        for obj in mm:
            committer_set.add(obj.commit.author.name)
            sha_set.add(obj.commit.sha)
            cnt = cnt + 1
            print(cnt)
    except ValueError:
        print("Oops! That was no valid number. Try again....")
    print(len(committer_set))
    print(len(sha_set))
    print(cnt)


def get_commits_countEx(token, repository):
    """
    repository='bitcoin/bitcoin'
    # https://api.github.com/repos/bitcoin/bitcoin/commits
    :param token
    :param repository: full name of github repo
    :rtype: :
    """
    g = Github(token)
    repo = g.get_repo(repository)

    mm = repo.get_commits('master', '', get_day_before(1), get_day_before(0))
    cnt = 0
    committer_set = set()
    sha_set = set()
    try:
        for obj in mm:
            committer_set.add(obj.commit.author.name)
            sha_set.add(obj.commit.sha)
            cnt = cnt + 1
            print(cnt)
    except ValueError:
        print("Oops! That was no valid number. Try again....")
    print(len(committer_set))
    print(len(sha_set))
    print(cnt)


# get_commits_count('a0f8dc4c9af976ed9e552f637ba1c25c326e24a2', 'bitcoin/bitcoin')

get_commits_countEx('a0f8dc4c9af976ed9e552f637ba1c25c326e24a2', 'bitcoin/bitcoin')

# get_commits('a0f8dc4c9af976ed9e552f637ba1c25c326e24a2')



