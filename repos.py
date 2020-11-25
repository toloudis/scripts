from dataclasses import dataclass
import subprocess
import sys
import traceback
from pathlib import Path


@dataclass
class Repos:
    url: str
    repos: list


repos_list = Repos(
    url="https://github.com/{}/{}.git",
    repos=[
        ("allen-cell-animated", "CellSwiper"),
        ("allen-cell-animated", "simularium-engine"),
        ("allen-cell-animated", "deepzoom_demo"),
        ("allen-cell-animated", "simularium-website"),
        ("allen-cell-animated", "integrated-mitotic-cell-scripts"),
        ("allen-cell-animated", "integrated-mitotic-viewer-prototype"),
        ("allen-cell-animated", "marion"),
        ("allen-cell-animated", "pca-viewer"),
        ("allen-cell-animated", "agave"),
        ("allen-cell-animated", "upy-scripts"),
        ("allen-cell-animated", "visual-essay-integrated-mitotic-cell"),
        ("allen-cell-animated", "website-3d-cell-viewer"),
        ("allen-cell-animated", "z-stack-scroller"),
        ("allen-cell-animated", "cell-feature-explorer"),
        ("allen-cell-animated", "simularium-viewer"),
        ("allen-cell-animated", "CellVRUnity"),
        ("allen-cell-animated", "integrated-cell-mitosis"),
        ("allen-cell-animated", "threejs-cell-test"),
        ("allen-cell-animated", "MolSimUnity"),
        ("allen-cell-animated", "ao-baking"),
        ("allen-cell-animated", "render-style-transfer"),
        ("allen-cell-animated", "CellAR"),
        ("allen-cell-animated", "cellbrowser-tools"),
        ("allen-cell-animated", "ivvv"),
        ("AllenCellModeling", "aicsimageio"),
        ("AllenCellModeling", "aicsimageprocessing"),
        ("AllenInstitute", "volume-viewer"),
        ("AllenInstitute", "cell-feature-data"),
    ],
)


def git_run(cmd_args, work_dir: Path = None):
    if work_dir is None:
        work_dir = "."
    if cmd_args[0] != "git":
        cmd_args.insert(0, "git")
    #
    try:
        subprocess.run(cmd_args, cwd=work_dir, universal_newlines=True)
    except subprocess.CalledProcessError:
        return False
    return True


def git_clone(repo_dir, remoterepo, parent_dir):
    if not repo_dir.exists():
        cmd_args = ["clone", remoterepo]
        return git_run(cmd_args, work_dir=parent_dir)
    else:
        git_pull(repo_dir, remoterepo, parent_dir)


def git_pull(repo_dir, remoterepo, parent_dir):
    # Get the current branch
    git_run(["pull", "--all"], work_dir=repo_dir)


def git_current_branch(repo_dir, remoterepo, parent_dir):
    git_run(["rev-parse", "--abbrev-ref", "HEAD"], work_dir=repo_dir)


def iterate_git(parent_dir, git_command):
    for r in repos_list.repos:
        project = r[0]
        repo = r[1]
        repo_dir: Path = parent_dir / repo
        remoterepo = repos_list.url.format(project, repo)
        print(f"\n{repo}")
        git_command(repo_dir, remoterepo, parent_dir)


# status
if __name__ == "__main__":
    try:
        # default windows 10 visual studio source code location, user-specific
        parent_dir = Path.home() / "source" / "repos"
        # iterate_git(parent_dir, git_current_branch)
        iterate_git(parent_dir, git_clone)
        # iterate_git(parent_dir, git_pull)
    except Exception as e:
        print("=============================================")
        print("\n\n" + traceback.format_exc())
        print("=============================================")
        print("\n\n" + str(e) + "\n")
        print("=============================================")
        sys.exit(1)
