"""
test_zyfun_sites.py
Test ZYFun config sites availability (HTTP reachable + valid JSON + data not empty)
"""
import json, re, sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== CONFIG ==========
ZYFUN_CONFIG = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\zyfun\zy_config_20260609.json"
OUTPUT_WORKING = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\__temp\zyfun_test_working.json"
OUTPUT_FAILED = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\__temp\zyfun_test_failed.json"
OUTPUT_STATS = r"D:\AI赋能中心\03_知识资产仓\个人生活\02_影音娱乐\02_影视源库\tvbox-source\__temp\zyfun_test_stats.json"

MAX_WORKERS = 30
TIMEOUT = 8

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


# ========== UTILITIES ==========
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def make_request(url, method="GET", timeout=TIMEOUT):
    """Send request, return (success, reason, status_code, content_preview)"""
    if not url or not url.startswith("http"):
        return False, "INVALID_URL", 0, ""
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.status
            raw = resp.read(1024 * 64)
            try:
                text = raw.decode("utf-8", errors="replace")
            except Exception:
                text = raw.decode("gbk", errors="replace")
            return True, "OK", status, text
    except urllib.error.HTTPError as e:
        return False, f"HTTP_{e.code}", e.code, ""
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if "timeout" in reason.lower():
            return False, "TIMEOUT", 0, ""
        if "name or service not known" in reason.lower():
            return False, "DNS_FAIL", 0, ""
        return False, f"URL_ERR:{reason[:30]}", 0, ""
    except Exception as e:
        return False, f"ERR:{str(e)[:30]}", 0, ""


def test_api_content(url):
    """GET api URL, check if returns valid JSON with non-empty list"""
    ok, reason, code, text = make_request(url, method="GET")
    if not ok:
        return ok, reason, ""

    text = text.strip()
    if not text:
        return False, "EMPTY", ""

    # Remove JSONP callback
    text = re.sub(r'^[^(]+\(', '', text)
    text = re.sub(r'\);?\s*$', '', text)
    text = text.strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return False, "NOT_JSON", ""

    # Check for video API format
    if isinstance(data, dict):
        for key in ["list", "data", "vod_list", "results"]:
            if key in data and data[key]:
                val = data[key]
                if isinstance(val, list) and len(val) > 0:
                    return True, "OK", text[:200]
                elif isinstance(val, (dict, str)) and val:
                    return True, "OK", text[:200]
        return False, "NO_LIST", ""
    elif isinstance(data, list):
        if len(data) > 0:
            return True, "OK", text[:200]
        return False, "EMPTY_LIST", ""
    else:
        return False, f"UNKNOWN_TYPE:{type(data).__name__}", ""


def test_site(site):
    """Test single site, return result dict"""
    api = site.get("api", "").strip()
    key = site.get("key", site.get("name", ""))
    stype = site.get("type", 0)
    group = site.get("group", "")
    name = site.get("name", "")
    ext = site.get("ext", "")

    if not api:
        return None

    result = {
        "key": key,
        "name": name,
        "api": api,
        "type": stype,
        "group": group,
        "ext": ext,
    }

    if stype == 1:
        ok, reason, preview = test_api_content(api)
        result["status"] = "WORKING" if ok else f"FAIL_{reason}"
        result["detail"] = preview[:100] if preview else reason
        return result

    elif stype == 12:
        ok, reason, _, _ = make_request(api, method="HEAD")
        if ok:
            result["status"] = "REACHABLE"
            result["detail"] = "Script URL reachable (cannot verify execution)"
        else:
            result["status"] = f"FAIL_{reason}"
            result["detail"] = reason
        return result

    else:
        ok, reason, _, _ = make_request(api, method="HEAD")
        result["status"] = "WORKING" if ok else f"FAIL_{reason}"
        result["detail"] = reason
        return result


def run():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 60)
    print("ZYFun Sites Batch Test Tool")
    print("=" * 60)

    print(f"\nLoading: {ZYFUN_CONFIG}")
    data = load_json(ZYFUN_CONFIG)
    sites = data.get("site", [])
    print(f"Total sites found: {len(sites)}\n")

    testable = [s for s in sites if s.get("api", "").strip()]
    print(f"Testable sites (with api field): {len(testable)}")

    type_counts = {}
    for s in testable:
        t = s.get("type", 0)
        type_counts[t] = type_counts.get(t, 0) + 1
    print("Type distribution:", {str(k): v for k, v in sorted(type_counts.items())})

    print(f"\nStarting test (workers={MAX_WORKERS}, timeout={TIMEOUT}s)...")
    print("-" * 60)

    results = []
    fail_count = 0
    ok_count = 0
    skip_count = len(sites) - len(testable)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(test_site, s): s for s in testable}

        for i, fut in enumerate(as_completed(futures), 1):
            res = fut.result()
            if res is None:
                continue

            status = res["status"]
            if status == "WORKING" or status == "REACHABLE" or ("NO_LIST" not in status and not status.startswith("FAIL")):
                ok_count += 1
                results.append(("OK", res))
            else:
                fail_count += 1
                results.append(("FAIL", res))

            if i % 100 == 0 or i == len(testable):
                print(f"  Progress: {i}/{len(testable)} | OK: {ok_count} | FAIL: {fail_count}")

    print("-" * 60)
    print(f"\nTest Complete!")
    print(f"  Total sites: {len(sites)}")
    print(f"  Skipped (no api): {skip_count}")
    print(f"  Tested: {len(testable)}")
    print(f"  [OK]: {ok_count}")
    print(f"  [FAIL]: {fail_count}")

    working = [r for tag, r in results if tag == "OK"]
    failed = [r for tag, r in results if tag == "FAIL"]

    save_json(OUTPUT_WORKING, working)
    save_json(OUTPUT_FAILED, failed)

    type_stats = {}
    for tag, r in results:
        t = r.get("type", 0)
        if t not in type_stats:
            type_stats[t] = {"total": 0, "ok": 0}
        type_stats[t]["total"] += 1
        if tag == "OK":
            type_stats[t]["ok"] += 1

    group_stats = {}
    for tag, r in results:
        g = r.get("group", "") or "default"
        if g not in group_stats:
            group_stats[g] = {"total": 0, "ok": 0}
        group_stats[g]["total"] += 1
        if tag == "OK":
            group_stats[g]["ok"] += 1

    stats = {
        "summary": {
            "total": len(sites),
            "testable": len(testable),
            "skip": skip_count,
            "ok": ok_count,
            "fail": fail_count,
            "ok_rate": round(ok_count / len(testable) * 100, 1) if testable else 0,
        },
        "by_type": {str(k): {
            "total": v["total"],
            "ok": v["ok"],
            "rate": round(v["ok"] / v["total"] * 100, 1)
        } for k, v in type_stats.items()},
        "by_group_top": sorted(
            [{"group": k, **v, "rate": round(v["ok"] / v["total"] * 100, 1)}
             for k, v in group_stats.items() if v["total"] >= 3],
            key=lambda x: x["rate"],
            reverse=True
        )[:20],
    }
    save_json(OUTPUT_STATS, stats)

    print(f"\nOutput files:")
    print(f"  [OK]   working sites : {OUTPUT_WORKING} ({len(working)})")
    print(f"  [FAIL] failed sites  : {OUTPUT_FAILED} ({len(failed)})")
    print(f"  [STAT] report        : {OUTPUT_STATS}")
    print("\nDone!")

    fail_reasons = {}
    for r in failed:
        status = r.get("status", "")
        fail_reasons[status] = fail_reasons.get(status, 0) + 1
    if fail_reasons:
        print(f"\nFailure reason breakdown:")
        for reason, cnt in sorted(fail_reasons.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {cnt:3d}x {reason}")


if __name__ == "__main__":
    run()
