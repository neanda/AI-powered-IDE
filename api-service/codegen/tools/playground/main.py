from typing import Any, List, Tuple
from langchain.tools import BaseTool

from session.playground.nodejs import NodeJSPlayground
from codegen.tools.playground.mock.request import MockRequestFactory
from session.session import GetEnvs

from .tools.filesystem import create_filesystem_tools
from .tools.process import create_process_tools
from .tools.code import create_code_tools


def create_playground_tools(
    method: str,
    route: str,
    request_body_template: str | None,
    get_envs: GetEnvs,
) -> Tuple[List[BaseTool], NodeJSPlayground]:
    playground = NodeJSPlayground(get_envs)

    mock = MockRequestFactory(
        method=method,
        route=route,
        body_template=request_body_template,
        playground=playground,
    )

    subtools: List[Any] = [
        tool
        for tools in (
            tool_factory(playground=playground, mock=mock)
            for tool_factory in [
                # create_filesystem_tools,
                # create_process_tools,
                create_code_tools,
            ]
        )
        for tool in tools
    ]
    return subtools, playground
