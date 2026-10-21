# Reading MCP servers for their defaults

No benchmark here. This is the set of commands used to pull the current top MCP
repositories and read each project's own documentation for one question: what
happens if you install it and change nothing.

Everything reported in the post comes from the projects' own README and
SECURITY.md files. Nothing in it is an undisclosed flaw.

## Run

```bash
# the ranking the post starts from
gh api -X GET search/repositories \
  -f q='mcp server in:name,description stars:>500' \
  -f sort=stars -f order=desc -f per_page=25 \
  --jq '.items[] | "\(.stargazers_count)\t\(.full_name)\t\(.language)\t\(.pushed_at[:10])"'

# read one project's docs without cloning it
gh api repos/<owner>/<repo>/contents/README.md --jq '.content' | base64 -d \
  | grep -inE "0\.0\.0\.0|--host|bind|read-only|allowed.?dir|sandbox|dangerous"

gh api repos/modelcontextprotocol/modelcontextprotocol/contents/SECURITY.md \
  --jq '.content' | base64 -d | sed -n '23,75p'
```

## The four questions

1. What address does it bind with no configuration?
2. Does the project's own container image override that?
3. Is authentication on by default, and what disables it?
4. Is the configuration that constrains the model reachable *by* the model?

Question 4 is the one that produced the most surprising answer.
