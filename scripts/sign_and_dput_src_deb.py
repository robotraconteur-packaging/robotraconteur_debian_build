from pathlib import Path
import subprocess

def main():
    out_dir = Path("out")
    assert out_dir.is_dir(), "src_deb out directory not found"

    for d in out_dir.iterdir():
        changes = d.glob("*.changes")
        for c in changes:
            subprocess.check_call("debsign -kB63969702B88510D6BD7C3467E27BB2F509608B9 *.changes", cwd=d, shell=True)
            subprocess.check_call("dput -f ppa:robotraconteur/ppa *.changes", cwd=d, shell=True)

if __name__ == "__main__":
    main()