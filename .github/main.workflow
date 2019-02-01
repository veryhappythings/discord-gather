workflow "New workflow" {
  on = "push"
  resolves = ["Run tests"]
}

action "Build Image" {
  uses = "actions/docker/cli@c08a5fc9e0286844156fefff2c141072048141f6"
  args = "build -t veryhappythings/discord-gather:$GITHUB_SHA ."
}

action "Run tests" {
  uses = "actions/docker/cli@c08a5fc9e0286844156fefff2c141072048141f6"
  args = "run --env COVERALLS_REPO_TOKEN=$COVERALLS_REPO_TOKEN veryhappythings/discord-gather:$GITHUB_SHA make test-with-coverage"
  needs = ["Build Image"]
  secrets = ["COVERALLS_REPO_TOKEN"]
}
