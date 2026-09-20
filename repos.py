import os
import subprocess
import sys
import traceback
from pathlib import Path

githuburl = "https://github.com/{}/{}.git"
# githuburl = "git@github.com:{}/{}.git"
githubs_work = [
    ("allen-cell-animated", "vole-app"),
    ("allen-cell-animated", "z-stack-scroller"),
    ("allen-cell-animated", "threejs-cell-test"),
    ("allen-cell-animated", "pca-viewer"),
    ("allen-cell-animated", "marion"),
    ("allen-cell-animated", "upy-scripts"),
    ("allen-cell-animated", "integrated-mitotic-cell-scripts"),
    ("allen-cell-animated", "MolSimUnity"),
    ("allen-cell-animated", "ao-baking"),
    ("allen-cell-animated", "temporary-file-service"),
    ("simularium", "simularium-website"),
    ("simularium", "simularium-viewer"),
    ("simularium", "octopus"),
    ("simularium", "simularium-engine"),
    ("simularium", "simulariumio"),
    ("simularium", "nbsv"),
    ("simularium", "simulariumXR"),
    ("AllenCell", "timelapse-colorizer"),
    ("AllenCell", "tfe-data"),
    ("AllenCell", "agave"),
    ("AllenCell", "ansible-platform"),
    ("AllenCell", "cell-feature-explorer"),
    ("AllenCell", "cell-feature-data"),
    ("AllenCell", "internal-engineering-docs"),
    ("AllenCell", "biofile-segmentation"),
    ("AllenCell", "orchestra-planner"),
    ("AllenCell", "terraform-platform"),
    ("AllenCell", "vole-core"),
    ("AllenInstitute", "biofile-finder"),
    ("bioio-devs", "aicspylibczi"),
    ("bioio-devs", "bioio"),
    ("bioio-devs", "bioio-base"),
    ("bioio-devs", "cookiecutter-bioio-reader"),
    ("bioio-devs", "bioio-czi"),
    ("bioio-devs", "bioio-imageio"),
    ("bioio-devs", "bioio-lif"),
    ("bioio-devs", "bioio-nd2"),
    ("bioio-devs", "bioio-tifffile"),
    ("bioio-devs", "bioio-ome-tiff"),
    ("bioio-devs", "bioio-sldy"),
    ("bioio-devs", "bioio-ome-zarr"),
    ("bioio-devs", "bioio-bioformats"),
    ("bioio-devs", "bioio-conversion"),
]
githubs_personal = [
    ("antoineborensztejn", "Total-microscope"),
    ("toloudis", "headslayer"),
    ("toloudis", "biocomputeserver"),
    ("toloudis", "py_viewer"),
    ("toloudis", "RayTracingInVulkan"),
    ("toloudis", "raygbiv-electron"),
    ("toloudis", "vv-webgpu"),
    ("toloudis", "vole-core"),
    ("toloudis", "vole-app"),
    ("toloudis", "simularium-viewer"),
    ("toloudis", "simularium-website"),
    ("toloudis", "biofile-finder"),
    ("toloudis", "bioprism"),
    ("toloudis", "timelapse-colorizer"),
    ("toloudis", "cell-feature-explorer"),
    ("toloudis", "calendar"),
    ("toloudis", "painter"),
    ("toloudis", "heisenshadow"),
    ("toloudis", "zarr-webgpu-multicanvas-demo"),
]


def git_run(cmd_args, work_dir: Path):
    if work_dir is None:
        work_dir = "."
    if cmd_args[0] != "git":
        cmd_args.insert(0, "git")
    #
    try:
        result = subprocess.run(cmd_args, cwd=work_dir, universal_newlines=True)
    except (subprocess.CalledProcessError, OSError):
        return False
    return result.returncode == 0


def git_clone(repo_dir, remoterepo, parent_dir):
    if not repo_dir.exists():
        repo_dir.mkdir(parents=True, exist_ok=True)
        cmd_args = ["clone", remoterepo]
        return git_run(cmd_args, work_dir=parent_dir)
    else:
        return git_pull(repo_dir, remoterepo, parent_dir)


def git_pull(repo_dir, remoterepo, parent_dir):
    # Get the current branch
    print(repo_dir)
    return git_run(["pull", "--all"], work_dir=repo_dir)


def git_current_branch(repo_dir, remoterepo, parent_dir):
    return git_run(["rev-parse", "--abbrev-ref", "HEAD"], work_dir=repo_dir)


def iterate_git(parent_dir: Path, git_command, githubs):
    failures = []
    for i in githubs:
        project = i[0]
        repo = i[1]
        repo_dir: Path = parent_dir / project / repo
        remoterepo = githuburl.format(project, repo)
        print(f"\n{project}/{repo}")
        try:
            result = git_command(repo_dir, remoterepo, parent_dir / project)
            if result is False:
                failures.append((f"{project}/{repo}", "git command reported failure"))
        except Exception as e:
            failures.append((f"{project}/{repo}", str(e)))
    return failures


# status
if __name__ == "__main__":
    try:
        which = sys.argv[1] if len(sys.argv) > 1 else "work"
        if which == "work":
            githubs = githubs_work
        elif which == "personal":
            githubs = githubs_personal
        else:
            print("Usage: python repos.py [work|personal]")
            sys.exit(1)

        # parent_dir = Path("/Users/danielt/src")
        # parent_dir = Path('C:\\Users\\danielt\\source\\repos')

        homedir = Path.home()
        osname = os.name
        if osname == "nt":
            parent_dir = Path(homedir / "source/repos")
        else:  # posix ... or java?
            parent_dir = Path(homedir / "src")

        print(f"Parent Dir: {parent_dir}\n\n")
        # failures = iterate_git(parent_dir, git_current_branch, githubs)
        failures = iterate_git(parent_dir, git_clone, githubs)
        # failures = iterate_git(parent_dir, git_pull, githubs)

        print("\n\n=============================================")
        if failures:
            print(f"{len(failures)} repo(s) failed:")
            for name, reason in failures:
                print(f"  - {name}: {reason}")
        else:
            print("All repos processed successfully.")
        print("=============================================")
    except Exception as e:
        print("=============================================")
        print("\n\n" + traceback.format_exc())
        print("=============================================")
        print("\n\n" + str(e) + "\n")
        print("=============================================")
        sys.exit(1)
