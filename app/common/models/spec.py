from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator


class Input(BaseModel):
    type: str = Field(..., description="Type of input (string, number, etc..,)")
    description: Optional[str] = Field(..., description="short description about input")
    required: bool = False


class PermissionSet(BaseModel):
    network: str = Field(..., description="Info about network access")
    filesystem: str = Field(
        ..., description="Info about file system (ephemeral, db, etc.,)"
    )
    tools: list[str] = Field(
        ...,
        description="List of tools that the spec has at its disposal",
    )


class Step(BaseModel):
    id: str = Field(..., description="Unique ID of the plan step")
    use: str = Field(..., description="Tool name to use (e.g. git.clone)")
    with_: dict[str, Any] = Field(
        default_factory=dict, alias="with", description="Input parameters to the tool"
    )
    output: Optional[str] = Field(None, description="Name of output variable")

    @field_validator("id")
    def no_spaces(cls, v: str):
        if " " in v:
            raise ValueError("Step id cannot contain spaces")
        return v


class Spec(BaseModel):
    version: str = Field(..., description="config version")
    capability: str = Field(..., description="info about capabiltiy of the spec")
    description: str = Field(..., description="short description about the capability")

    inputs: dict[str, Input] = Field(default_factory=dict)
    permissions: PermissionSet = Field(..., description="permissions and tools")
    returns: dict[str, str] = Field(
        ...,
        description="Return info for the spec (eg:  summary: ${{ summarize.output }})",
    )
