#!/usr/bin/env python3
"""IMPERIAL Core 26-repository main protection controller.

Stdlib only. Never stores/prints credentials. Defaults to read-only audit.
--plan: preflight actual successful GitHub check-run names for each repository.
--apply: requires explicit environment approval, independent reviewer confirmation,
         and successful check-run on main. Fails closed per repository.
--audit: verify effective branch protection, including exact required checks.

Use fine-grained GITHUB_TOKEN with Administration read for --plan/--audit,
Administration write for --apply. Never commit a token.
"""
import json, os, sys, urllib.request, urllib.error
OWNER="oromaskevic23-cmd"
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
REQUIRED_JOB="security-baseline"
def api(path, method="GET", data=None):
    token=os.environ.get("GITHUB_TOKEN")
    if not token: raise RuntimeError("GITHUB_TOKEN not configured")
    headers={"Authorization":"Bearer "+token,"Accept":"application/vnd.github+json",
             "X-GitHub-Api-Version":"2022-11-28","User-Agent":"imperial-protection-controller"}
    req=urllib.request.Request("https://api.github.com"+path,method=method,headers=headers,
        data=json.dumps(data).encode() if data is not None else None)
    try:
        with urllib.request.urlopen(req,timeout=25) as res:
            raw=res.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError("HTTP_"+str(e.code)) from None
def repo_path(name): return "/repos/"+OWNER+"/"+name
def preflight(name):
    base=repo_path(name)
    info=api(base)
    if info.get("default_branch")!="main": raise RuntimeError("MAIN_NOT_DEFAULT")
    head=api(base+"/branches/main")
    sha=head["commit"]["sha"]
    checks=api(base+"/commits/"+sha+"/check-runs?per_page=100")
    matching=[x for x in checks.get("check_runs",[]) if x.get("name")==REQUIRED_JOB
              and x.get("status")=="completed" and x.get("conclusion")=="success"]
    # Never assume a workflow title is the check context.
    return sha, bool(matching), [x.get("name") for x in checks.get("check_runs",[])]
def policy():
    return {
      "required_status_checks":{"strict":True,"contexts":[REQUIRED_JOB]},
      "enforce_admins":True,
      "required_pull_request_reviews":{"dismiss_stale_reviews":True,
        "require_code_owner_reviews":True,"required_approving_review_count":1,
        "require_last_push_approval":True},
      "restrictions":None,"required_linear_history":True,
      "allow_force_pushes":False,"allow_deletions":False,
      "required_conversation_resolution":True,"lock_branch":False,
      "allow_fork_syncing":False
    }
def verify(name):
    p=api(repo_path(name)+"/branches/main/protection")
    reviews=p.get("required_pull_request_reviews") or {}
    checks=p.get("required_status_checks") or {}
    return (p.get("enforce_admins",{}).get("enabled") is True
      and REQUIRED_JOB in checks.get("contexts",[])
      and checks.get("strict") is True
      and reviews.get("required_approving_review_count",0)>=1
      and reviews.get("require_code_owner_reviews") is True
      and reviews.get("dismiss_stale_reviews") is True
      and p.get("allow_force_pushes",{}).get("enabled") is False
      and p.get("allow_deletions",{}).get("enabled") is False)
def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("--plan","--audit","--apply"):
        raise SystemExit("Usage: protect_main.py --plan | --audit | --apply")
    mode=sys.argv[1]
    if mode=="--apply" and (os.getenv("IMPERIAL_OWNER_APPROVED")!="YES"
       or os.getenv("INDEPENDENT_REVIEWER_CONFIRMED")!="YES"):
        raise SystemExit("DENIED: explicit owner approval and independent reviewer confirmation required")
    failures=0
    for name in REPOS:
        try:
            if mode=="--audit":
                ok=verify(name)
                print(name, "VERIFIED" if ok else "INCOMPLETE")
            else:
                sha,ok,checks=preflight(name)
                if not ok:
                    print(name,"BLOCKED: successful security-baseline check absent on main; observed",checks[:12])
                elif mode=="--plan":
                    print(name,"READY_FOR_REVIEW",sha[:12],REQUIRED_JOB)
                else:
                    api(repo_path(name)+"/branches/main/protection","PUT",policy())
                    ok=verify(name)
                    print(name,"PROTECTION_VERIFIED" if ok else "WRITE_NOT_VERIFIED")
            failures+=not ok
        except Exception as exc:
            failures+=1
            print(name,"BLOCKED",str(exc)[:100])
    print("PASS",len(REPOS)-failures,"/",len(REPOS))
    return int(failures>0)
if __name__=="__main__":sys.exit(main())
