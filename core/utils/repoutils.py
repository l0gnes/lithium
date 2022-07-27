from os.path import exists, isdir
from os import mkdir, PathLike, listdir
from typing import Union, List
import git
import aiohttp
import re
import glob

def ensure_repos_directory_exists() -> None:
    
    if not exists('./repos/'):
        mkdir("./repos/")
    
def clone_repository(url : Union[str, PathLike], dest : Union[str, PathLike]) -> git.Repo:
    return git.Repo.clone_from(
        url, dest
    )

def check_for_valid_cog_tomls(repo_dir : Union[str, PathLike]) -> List[PathLike]:

    gl = glob.glob(
        f"{repo_dir}/*/cog.toml", recursive=False
    )

    return gl

async def fetch_github_repo_info(owner : str, repo_name : str) -> dict:
    
    async with aiohttp.ClientSession() as session:

        async with session.get(
            "https://api.github.com/repos/%s/%s" % (owner, repo_name)
        ) as resp:

            if resp.status == 200:

                return await resp.json()

    # TODO: Proper exceptions and respective handling should go here
    raise Exception

def decipher_github_uri(url : str) -> Union[List[str], None]:

    res = re.match(
        r"https:\/\/github\.com\/(?P<owner>[A-Za-z0-9-_]+)\/(?P<repo>[A-Za-z0-9-_]+)",
        url, 
    )

    if res:
        return res.group("owner"), res.group("repo")

    return None

def create_github_user_folder(user : str):
    if not exists("./repos/%s/" % (user)):
        mkdir("./repos/%s/" % (user))