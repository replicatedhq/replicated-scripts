#!/usr/bin/env python3

import argparse
import os
import sys

from github import Github


def update_team(token, team):
    team = team.lower()
    permissions = None
    # pull, push, admin, maintain, triage
    # https://docs.github.com/en/rest/teams/teams#add-or-update-team-repository-permissions
    permissions = {"engineering": "maintain", "customer-success": "admin", "sales": "pull"}
    if team not in permissions:
        print(f"Team {team} not setup with permissions")
        sys.exit(1)
    else:
        print(f"Setting {team} to {permissions}")

    g = Github(token)
    org = g.get_organization("replicated-collab")
    githubTeam = org.get_team_by_slug(team)

    for repo in org.get_repos(
        type="all"
    ):  # type: ‘all’, ‘public’, ‘private’, ‘forks’, ‘sources’, ‘member’
        print(
            f"Updating https://github.com/replciated-collab/{repo.name} : {permissions[team]}"
        )
        githubTeam.add_to_repos(repo)
        githubTeam.update_team_repository(repo, permissions[team])


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token",
        help="GitHub Access Token, defaults to environment GITHUB_ACCESS_TOKEN",
        default=os.environ["GITHUB_ACCESS_TOKEN"],
    )
    parser.add_argument("-t", help="The team to update", dest="team", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    update_team(args.token, args.team)
