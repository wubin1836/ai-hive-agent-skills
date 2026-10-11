#!/usr/bin/env python3
"""Offline result-record validation. It never authenticates, calls APIs, or executes actions.
Passing validates structure, local file hashes and explicit record invariants, not truth or tool capability.
"""
import argparse, hashlib, json, math, re, sys
from pathlib import Path
STATES={"planned","awaiting_user","ready","submitted","completed","accepted","review_required","failed","cancelled"}
KINDS={"plan","read","draft","generate","write_external","send","pay","delete"}
MUTATING={"write_external","send","pay","delete"}
SECRET=re.compile(r"(?:skh_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,}|ghp_[A-Za-z0-9]{20,})")

def validate(data,contract,artifact_root=None):
    errors=[]
    def err(message): errors.append(message)
    if not isinstance(data,dict): return ["root must be an object"]
    if data.get("skill_id")!=contract["skill_id"]:err("skill_id mismatch")
    if SECRET.search(json.dumps(data,ensure_ascii=False)):err("credential-like value detected; redact before saving")
    rows=data.get("records")
    if not isinstance(rows,list) or not rows:return errors+["records must be a non-empty list"]
    seen=set()
    for i,r in enumerate(rows):
        prefix="record "+str(i)
        if not isinstance(r,dict):err(prefix+": not an object");continue
        rid=r.get("id")
        if not isinstance(rid,str) or not rid.strip():err(prefix+": missing id")
        elif rid in seen:err(prefix+": duplicate id")
        else:seen.add(rid)
        status=r.get("status"); kind=r.get("action_kind")
        if status not in STATES:err(prefix+": invalid status")
        if kind not in KINDS:err(prefix+": invalid action_kind")
        if not isinstance(r.get("executed"),bool):err(prefix+": executed must be boolean")
        if r.get("executed") and kind in MUTATING and not str(r.get("authorization_ref") or "").strip():
            err(prefix+": external mutation requires authorization reference")
        if status in {"completed","accepted"} and not r.get("executed"):
            err(prefix+": cannot complete an unexecuted action")
        if status in {"planned","awaiting_user","ready"} and r.get("executed"):
            err(prefix+": pre-execution status contradicts executed=true")
        evidence=r.get("evidence")
        if not isinstance(evidence,list) or any(not isinstance(x,str) or not x.strip() for x in evidence):
            err(prefix+": evidence must contain non-empty string references")
        elif status in {"completed","accepted"} and not evidence:err(prefix+": completion lacks evidence")
        if r.get("execution_level") not in {"plan_only","local_result","external_receipt"}:
            err(prefix+": invalid execution_level")
        if status in {"completed","accepted"} and r.get("execution_level")=="plan_only":
            err(prefix+": a plan alone is not an executed result")
        if status in {"completed","accepted"} and kind in MUTATING and r.get("execution_level")!="external_receipt":
            err(prefix+": external mutation completion needs external receipt level")
        if r.get("execution_level")=="external_receipt" and status in {"completed","accepted"} and not str(r.get("provider_task_id") or "").strip():
            err(prefix+": external completion lacks provider receipt")
        if status=="accepted" and r.get("checked") is not True:err(prefix+": accepted needs checked=true")
        domain=r.get("domain")
        if not isinstance(domain,dict):err(prefix+": domain must be object");continue
        for field in contract["fields"]:
            cell=domain.get(field)
            if not isinstance(cell,dict):err(prefix+": missing domain cell "+field);continue
            state=cell.get("state")
            if state not in {"known","unknown","not_applicable"}:err(prefix+": invalid cell state "+field)
            value=cell.get("value")
            if isinstance(value,float) and not math.isfinite(value):err(prefix+": non-finite value "+field)
            if state=="known":
                if value is None or value=="":err(prefix+": known field lacks value "+field)
                if not str(cell.get("source_ref") or "").strip():err(prefix+": known field lacks provenance "+field)
            if state=="not_applicable" and not str(cell.get("reason") or "").strip():
                err(prefix+": not_applicable needs reason "+field)
            if state=="unknown" and status=="accepted":err(prefix+": unresolved field cannot be accepted "+field)
        artifacts=r.get("artifacts")
        if not isinstance(artifacts,list):err(prefix+": artifacts must be list");continue
        if status in {"completed","accepted"} and not artifacts:err(prefix+": completion lacks deliverable")
        for a in artifacts:
            if not isinstance(a,dict) or not isinstance(a.get("path"),str):
                err(prefix+": invalid artifact");continue
            if not re.fullmatch(r"[0-9a-f]{64}",str(a.get("sha256",""))):
                err(prefix+": artifact lacks SHA-256");continue
            if Path(a["path"]).is_absolute():
                err(prefix+": artifact path must be relative");continue
            if artifact_root is not None:
                root=Path(artifact_root).resolve()
                target=(root/a["path"]).resolve()
                try:target.relative_to(root)
                except ValueError:err(prefix+": artifact outside allowed root");continue
                if not target.is_file():err(prefix+": artifact missing");continue
                if target.stat().st_size>100_000_000:err(prefix+": artifact too large for this checker");continue
                if hashlib.sha256(target.read_bytes()).hexdigest()!=a["sha256"]:err(prefix+": artifact hash mismatch")
    return errors

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("result",type=Path)
    ap.add_argument("--artifact-root",type=Path)
    args=ap.parse_args()
    try:
        contract=json.loads((Path(__file__).resolve().parents[1]/"assets"/"output-contract.json").read_text())
        data=json.loads(args.result.read_text())
        errors=validate(data,contract,args.artifact_root or args.result.parent)
    except (OSError,ValueError,KeyError) as exc:
        print(json.dumps({"valid":False,"error_type":type(exc).__name__}));return 2
    print(json.dumps({"valid":not errors,"errors":errors,"scope":"structure/provenance/local-file checks only; no live actions tested"},ensure_ascii=False))
    return 1 if errors else 0
if __name__=="__main__":sys.exit(main())
