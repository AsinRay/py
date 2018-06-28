import datetime
from dateutil.relativedelta import relativedelta
from github import Github


class PyGithubSpider:

    token = 'a0f8dc4c9af976ed9e552f637ba1c25c326e24a2'

    def __init__(self, token, org, repo):
        self.token = token
        self.org = org
        self.repo = repo
        self.full_repo_name = org + '/' + repo

    def get_month_before(self, before, basepoint=datetime.datetime.now()):
        """
        :param self
        :param before: int
        :param basepoint: datetime.datetime
        :rtype: :class: datetime
        """
        return basepoint - relativedelta(months=+before)

    def get_day_before(self, before, basepoint=datetime.datetime.now()):
        """
        :param self
        :param before: int
        :param basepoint: datetime.datetime
        :rtype: :class: datetime
        """
        return basepoint - relativedelta(days=+before)

    def get_stargazers(self, token,repository='bitcoin/bitcoin'):
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

    def get_commits(self, token,repository='bitcoin/bitcoin'):
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

    def get_commits_count(self, token, repository='bitcoin/bitcoin'):
        """
        # https://api.github.com/repos/bitcoin/bitcoin/commits
        :param token
        :param repository: full name of github repo
        :rtype: :
        """
        g = Github(token)
        repo = g.get_repo(repository)

        mm = repo.get_commits('master', '', get_month_before(1))
        cnt = 0
        committer_set = set()
        for obj in mm:
            print(obj.committer.login)
            committer_set.add(obj.committer.login)
            cnt = cnt + 1
        print(len(committer_set))
        print(cnt)

    # get_commits_count(thi, 'EOSIO/eos')

# get_commits('a0f8dc4c9af976ed9e552f637ba1c25c326e24a2')



