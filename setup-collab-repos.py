#!/usr/bin/env python3

import argparse
import os

from github import Github


class GithubOrg:
    def __init__(self, token, name) -> None:
        self.name = name
        self.gh = Github(token)
        self.org = self.gh.get_organization(name)

    def set_permissions(self, permissions):
        # pull, push, admin, maintain, triage
        # https://docs.github.com/en/rest/teams/teams#add-or-update-team-repository-permissions
        perms = {k.lower(): v.lower() for k, v in permissions.items()}
        self.permissions = perms

    def update_teams(self):
        for team, permission in self.permissions.items():
            print(f"Setting {team} to {permission}")
            githubTeam = self.org.get_team_by_slug(team)

            for repo in self.org.get_repos(
                type="all"
            ):  # type: ‘all’, ‘public’, ‘private’, ‘forks’, ‘sources’, ‘member’
                print(
                    f"Updating https://github.com/{self.org}/{repo.name} : {permission}"
                )
                githubTeam.add_to_repos(repo)
                githubTeam.update_team_repository(repo, permission)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token",
        help="GitHub Access Token, defaults to environment GITHUB_ACCESS_TOKEN",
        default=os.environ["GITHUB_ACCESS_TOKEN"],
    )
    parser.add_argument(
        "--orgs",
        help="The orgs to update",
        dest="orgs",
        nargs="+",
        default=["replicated-collab", "replicated-collab-dev"],
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    if "replicated-collab" in args.orgs:
        print("Processing replicated-collab")
        permissions = {
            "engineering": "maintain",
            "customer-success": "admin",
            "sales": "triage",
        }
        org = GithubOrg(args.token, "replicated-collab")
        org.set_permissions(permissions)
        org.update_teams()

    if "replicated-collab-dev" in args.orgs:
        print("Processing replicated-collab-dev")
        permissions = {"engineering": "maintain", "ce-team": "maintain"}
        org = GithubOrg(args.token, "replicated-collab-dev")
        org.set_permissions(permissions)
        org.update_teams()
