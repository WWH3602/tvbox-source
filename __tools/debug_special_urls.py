import subprocess, sys, os

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36"

# 测试南风和饭太硬 用 curl-v 看看 TLS 详情
TESTS = [
    ("南风-ghproxy", "https://ghproxy.net/https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"),
    ("南风-直连", "https://raw.githubusercontent.com/yoursmile66/TVBox/main/XC.json"),
    ("饭太硬-中文", "http://xn--4gqvb6h.xn--fiqs8s/tv"),
    ("饭太硬-http", "http://www.fanTaiying.com/tv"),
    ("饭太硬-备用", "http://tv.fanTaiYing.xyz/tv"),
    ("肥猫-puny", "http://xn--fiqs8s.xn--fiqs8s/"),
    ("肥猫-http", "http://feimao.best/"),
    ("小米-mpanso", "https://mpanso.me/DEMO.json"),
    ("菜妮丝", "https://tvbox.cainisi.cc"),
]

for name, url in TESTS:
    print(f"\n[{name}]")
    cmd = ["curl", "-sI", "-L", "-A", UA,
           "--tlsv1.2", "--tls-max", "1.2",
           "-m", "15", "-w", "HTTP:%{http_code} SIZE:%{size_download}",
           url]
    r = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace', timeout=20)
    print(f"  -> {r.stdout[:200]}")
    if r.stderr:
        print(f"  err: {r.stderr[:100]}")
