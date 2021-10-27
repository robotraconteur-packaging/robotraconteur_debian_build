from pathlib import Path
import argparse
import re
import os
from github import Github
import subprocess
import datetime
from git import Repo

def main():
    
    parser = argparse.ArgumentParser(description="Update package new version")
    parser.add_argument("--dest-repository", type=str, default=None, help="The source repository")
    parser.add_argument("--token-file", type=argparse.FileType("r"), help="Load token from file")
    parser.add_argument("--dirty",action="store_true",help="Ignore dirty repo")

    args = parser.parse_args()

    assert Path("robotraconteur_debian_build/scripts/make_release.py").is_file(), "Must run script from work root"

    token = None

    if args.token_file:        
        token = args.token_file.read().strip()

    if token is None:
        token = os.environ.get("BOT_GITHUB_TOKEN", None)

    assert token, "Invalid bot token"

    with open("robotraconteur_debian_build/upstream_tag_name","r") as f:
        upstream_tag_name = f.read().strip()

    print(upstream_tag_name)

    tag_name = upstream_tag_name + "-" + datetime.datetime.now().strftime("%Y%m%d")

    subprocess.check_call("tar cf ../srcdebs.tar.gz *", shell=True, cwd="out")
    subprocess.check_call("tar cf ../debs.tar.gz *", shell=True, cwd="bin_out")

    repo = args.dest_repository
    if repo is None:
        repo = os.environ["INPUT_DEST_REPOSITORY"]

    local_repo = Repo("robotraconteur_debian_build")
    print(local_repo.head.commit)

    if not args.dirty:
        assert not local_repo.is_dirty(), "Repo is dirty"
        assert len(local_repo.untracked_files) == 0, "Repo is dirty"

    existing_tag_names = [t.name for t in local_repo.tags]

    tag_name2 = tag_name    
    if tag_name2 in existing_tag_names:
        i = 1
        while tag_name2 in existing_tag_names:
            tag_name2 = f"{tag_name}-{i}"
            i+=1

    print(tag_name2)

    new_tag = local_repo.create_tag(tag_name2,message=tag_name)

    local_repo.git.push(f"git@github.com:{repo}.git", tags=True)

    github = Github(token)
    repo = github.get_repo(repo)
    release = repo.create_git_release(tag_name2, tag_name2, tag_name2)
    release.upload_asset("debs.tar.gz", name="debs.tar.gz", content_type='application/binary')
    release.upload_asset("srcdebs.tar.gz", name="debs.tar.gz", content_type='application/binary')



if __name__ == "__main__":
    main()