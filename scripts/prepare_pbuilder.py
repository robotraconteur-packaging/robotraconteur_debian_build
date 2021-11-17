import subprocess
import platform

machine = platform.machine()

if machine == 'x86_64':
    build_configs = [
        ("debian","buster","amd64"),        
        ("debian","bullseye","amd64"),  
    ]

if machine == 'aarch64':
    build_configs = [
        ("debian","buster","arm64"),
        ("debian","buster","armhf"),
        ("raspbian","buster","armhf"),
        ("debian","bullseye","arm64"),
        ("debian","bullseye","armhf"),
        ("raspbian","bullseye","armhf")    
    ]

for c in build_configs:

    os, dist, arch = c

    subprocess.check_call(f"sudo mkdir -p /var/cache/pbuilder/{os}-{dist}-{arch}/aptcache/", shell=True)
    subprocess.check_call(f"sudo OS={os} DIST={dist} ARCH={arch} pbuilder --create", shell=True)