from pathlib import Path
import subprocess
import shutil

build_configs = [
    ("debian","buster","amd64"),
    ("debian","buster","arm64"),
    ("debian","buster","armhf"),
    ("raspbian","buster","amd64")
]

def main():
    bin_work = Path("bin_work")
    if bin_work.exists():
        shutil.rmtree(bin_work)
    bin_work.mkdir()

    for c in build_configs:

        os, dist, arch = c

        src_deb1 = list(Path(F"out/{dist}").absolute().glob(f"*{dist}.dsc"))
        assert len(src_deb1) == 1, "Could not find source deb"
        src_deb = src_deb1[0].absolute()
        
        work_dir_name = f"{os}-{dist}-{arch}"
        work_dir = bin_work.joinpath(work_dir_name)
        
        subprocess.check_call(f"dpkg-source -x {src_deb} {work_dir_name}", shell=True, cwd=bin_work)

        subprocess.check_call(f"OS={os} DIST={dist} ARCH={arch} pdebuild", shell=True, cwd=work_dir)

    subprocess.check_call("sudo chown wasonj -R *", shell=True, cwd=bin_work)
    subprocess.check_call("find . -name *dbgsym* -exec rm {} \;", shell=True, cwd=bin_work)

if __name__ == "__main__":
    main()