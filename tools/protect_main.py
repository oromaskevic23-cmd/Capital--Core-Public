#!/usr/bin/env python3
"""Read-only by default. Apply GitHub main protection with explicitly approved admin token.
Requires Python 3 stdlib, env GITHUB_TOKEN with Administration write rights.
Does not print tokens or response bodies.
"""
import os,json,urllib.request,urllib.error,sys
REPOS="""IMPERIAL-Core-
Repository-name-IMPERIAL-Core
HANTER
Nano-Core-Agents
Enterprise-IMPERIAL-Skills
Codex-Enterprise-IMPERIAL-Skills
IMPERIAL-Core-Public
IMPERIAL-Engineering-Intelligence-
HANTER-Public
Nano-Core-Agents-Public
Codex--PRIVATE-
Legion-Public
CRYPTO-IMPERIAL-Ecosystem-Public
ORION-Public
IMPERIAL-AGI
CYBER-HAK-Public
VELION-LLM-Public
AGY---PUBLIC-
mirofish
lingbot-vla-v2
CONSTRUCTOR-AI
SHPAIZMAN-ORCHESTRATOR
IMPERIAL-Core-US-HoldCo-Founder-Control-Blueprint
oromaskevic23-cmd
Jem-
IMPERIAL-Venture-Factory""".splitlines()
OWNER="oromaskevic23-cmd"
def request(path,method="GET",data=None):
    token=os.environ["GITHUB_TOKEN"]
    req=urllib.request.Request("https://api.github.com"+path,
        headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
                 "X-GitHub-Api-Version":"2022-11-28","User-Agent":"imperial-enterprise-protection"},
        method=method,data=json.dumps(data).encode() if data is not None else None)
    with urllib.request.urlopen(req,timeout=20) as response:
        body=response.read()
        return json.loads(body) if body else {}
def target(repo):
    return "/repos/"+OWNER+"/"+repo+"/branches/main/protection"
def policy(checks):
    return {
      "required_status_checks":{"strict":True,"contexts":checks},
      "enforce_admins":True,
      "required_pull_request_reviews":{"dismiss_stale_reviews":True,
          "require_code_owner_reviews":True,"required_approving_review_count":1,
          "require_last_push_approval":True},
      "restrictions":None,
      "required_linear_history":True,
      "allow_force_pushes":False,
      "allow_deletions":False,
      "required_conversation_resolution":True,
      "lock_branch":False,
      "allow_fork_syncing":False
    }
def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("--audit","--apply"):
        raise SystemExit("Usage: python3 protect_main.py --audit | --apply")
    if not os.getenv("GITHUB_TOKEN"):
        raise SystemExit("GITHUB_TOKEN missing: no changes made")
    apply=sys.argv[1]=="--apply"
    print("Mode:", "APPLY" if apply else "READ-ONLY AUDIT")
    failures=0
    for repo in REPOS:
        path=target(repo)
        try:
            if apply:
                # A required check must be observed as successful on the actual default branch
                # before it is configured; avoid permanently blocking merges with invented names.
                print(repo, "NOT_APPLIED: verify exact required CI context and independent reviewer first")
                failures+=1
                continue
            p=request(path)
            reviews=p.get("required_pull_request_reviews") or {}
            checks=p.get("required_status_checks") or {}
            ok=bool(p.get("enforce_admins",{}).get("enabled") and
                reviews.get("required_approving_review_count",0)>=1 and
                reviews.get("require_code_owner_reviews") and
                checks.get("contexts") and
                not p.get("allow_force_pushes",{}).get("enabled") and
                not p.get("allow_deletions",{}).get("enabled"))
            print(repo,"PROTECTED" if ok else "INCOMPLETE")
            failures+=not ok
        except urllib.error.HTTPError as e:
            print(repo,"UNVERIFIED_HTTP_"+str(e.code))
            failures+=1
    print("Verified:",len(REPOS)-failures,"/",len(REPOS))
    return 1 if failures else 0
if __name__=="__main__":sys.exit(main())
