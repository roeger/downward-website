#! /usr/bin/env python3

import json
import logging
import os
from pathlib import Path
import shutil
import subprocess
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT_DIR = SCRIPT_DIR.parents[0]
TMP_MARKDOWN = "tmp_markdown"
WEBSITE = "site"
GIT_USER = "build_website"
GIT_EMAIL = "no_email@example.com"

def copy_main_content(tmp_markdown):
    try:
        shutil.copytree(REPO_ROOT_DIR/"docs", tmp_markdown/"main-docs")
    except OSError as e:
        sys.exit(e)
    try:
        shutil.copy(REPO_ROOT_DIR/"mkdocs.yml", tmp_markdown/"mkdocs.yml")
    except OSError as e:
        sys.exit(e)

def init_git_repo(tmp_markdown):
    os.chdir(tmp_markdown)
    cmd = ["git", "init"]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)

    cmd = ["git", "config", "user.name", f"'{GIT_USER}'"]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
    cmd = ["git", "config", "user.email", f"'{GIT_EMAIL}'"]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)

def create_revision_website(tmp_markdown, revision, alias=None):
    logging.info(f"building version {revision}...")
    branch_name = revision
    if revision == "HEAD":
        branch_name = "head-docs"
    else:
        branch_name = f"release-{revision}"

    try:
        os.chdir(REPO_ROOT_DIR)
    except FileNotFoundError:
        logging.critical(f"Directory: {REPO_ROOT_DIR} does not exist")
        return
    except PermissionError:
        logging.critical(f"You do not have permissions to change to {REPO_ROOT_DIR}")
        return

    doc_dir =  tmp_markdown/revision/"docs"
    archive_cmd = ["git", "archive", "--format=tar",
                   f"--output={tmp_markdown}/archive.tar", branch_name, "docs"]
    untar_cmd = ["tar", "xf", "archive.tar", "-C", doc_dir]
    try:
        subprocess.check_call(archive_cmd)
    except subprocess.CalledProcessError:
        print(f"Could not obtain branch for {revision}. Skipping it...")
        return
    doc_dir.mkdir(parents=True)
    os.chdir(tmp_markdown)
    subprocess.check_call(untar_cmd)
    os.chdir(tmp_markdown/revision/"docs")
    (doc_dir/"docs").rename(doc_dir/"documentation")
    for child in (tmp_markdown/"main-docs").iterdir():
        os.symlink(child, child.name)
    os.chdir(tmp_markdown/revision)
    os.symlink(tmp_markdown/"mkdocs.yml", "mkdocs.yml")
    os.chdir(tmp_markdown)
    cmd = ["git", "add", f"{revision}/"]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
    cmd = ["git", "commit", "-m", f"adding revision {revision}"]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
    os.chdir(tmp_markdown/revision)
    if alias is not None:
        cmd = ["mike", "deploy", revision, alias]
    else:
        cmd = ["mike", "deploy", revision]
    subprocess.check_call(cmd)
    if alias is not None:
        cmd = ["mike", "set-default", "latest"]
        subprocess.run(cmd)

def create_revision_websites(markdown_dir):
    with open(REPO_ROOT_DIR/'releases.json') as f:
        releases = json.load(f)
        for r in releases:
            create_revision_website(tmp_markdown_dir, r["release"], r.get("alias"))

def collect_result(tmp_markdown, outdir):
    os.chdir(tmp_markdown)
    archive_cmd = ["git", "archive", "--format=zip",
                   f"--output={outdir}/site.zip", "gh-pages"]
    subprocess.check_call(archive_cmd)

def post_process_result(outdir):
    # move the img folder from the HEAD version on level higher and
    # replace the copies of the img folder in all versions with
    # a symbolic link to that one.
    # Proceed analgously for "files" and "assets" folders.
    releases = set()
    with open(REPO_ROOT_DIR/'releases.json') as f:
        releases = set(r["release"] for r in json.load(f))
    os.chdir(outdir)
    tmp_dir = outdir/"site"
    tmp_dir.mkdir()
    subprocess.check_call(["unzip", "site.zip", "-d", tmp_dir])
    (outdir/"site.zip").unlink()

    for folder in ("img", "files", "assets"):
        if (tmp_dir/"HEAD"/folder).exists():
            shutil.move(tmp_dir/"HEAD"/folder, tmp_dir/folder)
            os.chdir(tmp_dir)
            for child in (tmp_dir).iterdir():
                if child.is_dir() and child.name in releases:
                    if (child/folder).exists():
                        shutil.rmtree(child/folder)
                    os.symlink(f"../{folder}", child/folder)

    os.chdir(tmp_dir)
    subprocess.check_call("zip -yr ../site.zip .", shell=True)
    shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("building website...")
    tmp_markdown_dir = SCRIPT_DIR / TMP_MARKDOWN
    outdir = SCRIPT_DIR / WEBSITE
    try:
        outdir.mkdir()
        tmp_markdown_dir.mkdir()
    except FileExistsError as e:
        sys.exit(e)
    copy_main_content(tmp_markdown_dir)
    init_git_repo(tmp_markdown_dir)
    create_revision_websites(tmp_markdown_dir)
    collect_result(tmp_markdown_dir, outdir)
    post_process_result(outdir)
#    shutil.rmtree(tmp_markdown_dir)
