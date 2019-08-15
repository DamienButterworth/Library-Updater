#!/usr/bin/env python3

import json
import os
from typing import Optional

from graphqlclient import GraphQLClient


class HmrcReleaseSearch:
    def __init__(self):
        self.client = GraphQLClient('https://api.github.com/graphql')
        oauth_token = os.environ.get('GITOAUTH')  # type: Optional[str]

        if not oauth_token:
            print("environment variable $GITOAUTH is not defined")
            exit(1)

        if not oauth_token.startswith("Bearer"):
            print("environment variable $GITOAUTH does not start with 'Bearer'")
            exit(1)

        self.client.inject_token(oauth_token)  # OauthToken 'bearer {token}'

    def graph_ql_search(self, lib_name):
        return self.client.execute('''
                    query {
                      repository(owner:"hmrc", name:"''' + lib_name + '''") {
                        releases(first: 100, orderBy: {direction: DESC, field: CREATED_AT}) {
                                nodes {
                            name
                          }
                        }
                      }
                    }
                    ''')

    def fetch_release(self, sbt_version, library_name, current_version, domain):
        if domain == "uk.gov.hmrc":
            version_number = current_version.replace("-play-25", "").replace("-play-26", "")

            for release in json.loads(self.graph_ql_search(library_name))["data"]["repository"]["releases"]["nodes"]:
                release_name = str(release["name"])
                test = version_number
                release_number = str(
                    release_name.replace("-play-25", "").replace("-play-26", "").replace(",", "").split(" ")[0])
                if test.split(".")[0] == release_number.split(".")[0]:
                    if "-play-25" in release_name:
                        if "2.5" in sbt_version:
                            return str(release_number + "-play-25")
                        else:
                            return str(release_number + "-play-26")
                    else:
                        return str(release_number)
