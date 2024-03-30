import subprocess
import sys
import traceback
from pathlib import Path

githuburl = "https://github.com/{}/{}.git"
#githuburl = "git@github.com:{}/{}.git"
githubs = [
    ("allen-cell-animated", "nucmorph-colorizer"),
    ("allen-cell-animated", "agave"),
    ("allen-cell-animated", "website-3d-cell-viewer"),
    ("allen-cell-animated", "colorizer-data"),
    ("allen-cell-animated", "cellbrowser-tools"),
    ("allen-cell-animated", "cell-feature-data"),
    ("allen-cell-animated", "volume-viewer"),
    ("allen-cell-animated", "cell-feature-explorer"),
    ("allen-cell-animated", "nbvv"),
    ("allen-cell-animated", "deepzoom_demo"),
    ("allen-cell-animated", "z-stack-scroller"),
    ("allen-cell-animated", "threejs-cell-test"),
    ("allen-cell-animated", "pca-viewer"),
    ("allen-cell-animated", "marion"),
    ("allen-cell-animated", "upy-scripts"),
    ("allen-cell-animated", "integrated-mitotic-cell-scripts"),
    ("allen-cell-animated", "MolSimUnity"),
    ("allen-cell-animated", "ao-baking"),
    ("allen-cell-animated", "render-style-transfer"),
    ("simularium", "simularium-website"),
    ("simularium", "simularium-viewer"),
    ("simularium", "octopus"),
    ("simularium", "simularium-engine"),
    ("simularium", "simulariumio"),
    ("simularium", "nbsv"),
    ("aics-int", "ome-zarr-conversion"),
    ("AllenCellModeling", "napari-aicsimageio"),
    ("AllenCellModeling", "aicsimageio"),
    ("AllenCellModeling", "aicsimageprocessing"),
    ("AllenCellModeling", "aicspylibczi"),
    ("bioio-devs", "bioio"),
    ("bioio-devs", "bioio-base"),
    ("bioio-devs", "cookiecutter-bioio-reader"),
    ("bioio-devs", "bioio-czi"),
    ("bioio-devs", "bioio-lif"),
    ("bioio-devs", "bioio-nd2"),
    ("bioio-devs", "bioio-tifffile"),
    ("bioio-devs", "bioio-ome-tiff"),
    ("bioio-devs", "bioio-sldy"),
    ("bioio-devs", "bioio-ome-zarr"),
    ("bioio-devs", "bioio-bioformats"),
    ("toloudis", "py_viewer"),
    ("toloudis", "RayTracingInVulkan"),
    ("toloudis", "raygbiv-electron")
]


def git_run(cmd_args, work_dir: Path = None):
    if work_dir is None:
        work_dir = '.'
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
        repo_dir.mkdir(parents=True, exist_ok=True)
        cmd_args = ["clone", remoterepo]
        return git_run(cmd_args, work_dir=parent_dir)
    else:
        git_pull(repo_dir, remoterepo, parent_dir)


def git_pull(repo_dir, remoterepo, parent_dir):
    # Get the current branch
    print(repo_dir)
    git_run(["pull", "--all"], work_dir=repo_dir)


def git_current_branch(repo_dir, remoterepo, parent_dir):
    git_run(["rev-parse", "--abbrev-ref", "HEAD"], work_dir=repo_dir)


def iterate_git(parent_dir, git_command):
    for i in githubs:
        project = i[0]
        repo = i[1]
        repo_dir: Path = parent_dir / project / repo
        remoterepo = githuburl.format(project, repo)
        print(f"\n{project}/{repo}")
        git_command(repo_dir, remoterepo, parent_dir / project)


# status
if __name__ == "__main__":
    try:
        parent_dir = Path('C:\\Users\\danielt\\source\\repos')
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
