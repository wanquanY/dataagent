from dataclasses import dataclass
from functools import wraps
from textwrap import dedent
from typing import Any, Callable, Optional

import click


def require_workspace():
    def require_workspace_inner(f: Callable[..., None]):
        @wraps(f)
        @click.pass_context
        def new_func(ctx: click.Context, *args: Any, **kwargs: Any):
            if ctx.obj.is_workspace_valid:
                return ctx.invoke(f, *args, **kwargs)
            else:
                click.echo(
                    "The current directory is not a valid Task Weaver project directory. "
                    "There needs to be a `taskweaver-config.json` in the root of the project directory. "
                    "Please change the working directory to a valid project directory or initialize a new one. "
                    "Refer to --help for more information.",
                )
                ctx.exit(1)

        return new_func

    return require_workspace_inner


@dataclass
class CliContext:
    workspace: Optional[str]
    workspace_param: Optional[str]
    is_workspace_valid: bool
    is_workspace_empty: bool


def get_ascii_banner() -> str:
    return dedent(
        r"""
#  $$$$$$\                                                                $$\     
# $$  __$$\                                                               $$ |    
# $$ /  \__|$$\   $$\ $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$\   
# \$$$$$$\  $$ |  $$ |$$  __$$\  \____$$\ $$  __$$\ $$  __$$\ $$  __$$\ \_$$  _|  
#  \____$$\ $$ |  $$ |$$ |  $$ | $$$$$$$ |$$ /  $$ |$$$$$$$$ |$$ |  $$ |  $$ |    
# $$\   $$ |$$ |  $$ |$$ |  $$ |$$  __$$ |$$ |  $$ |$$   ____|$$ |  $$ |  $$ |$$\ 
# \$$$$$$  |\$$$$$$$ |$$ |  $$ |\$$$$$$$ |\$$$$$$$ |\$$$$$$$\ $$ |  $$ |  \$$$$  |
#  \______/  \____$$ |\__|  \__| \_______| \____$$ | \_______|\__|  \__|   \____/ 
#           $$\   $$ |                    $$\   $$ |                              
#           \$$$$$$  |                    \$$$$$$  |                              
#            \______/                      \______/                                                            
        """,
    ).strip()
