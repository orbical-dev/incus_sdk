"""
Instance model for Incus resources.
"""

from typing import Dict, Any, List, Optional
from incus_sdk.models.base import Model


class Instance(Model):
    """Model representing an Incus instance (container or virtual machine)."""

    def __init__(
        self,
        client=None,
        name: str = None,
        architecture: str = None,
        config: Dict[str, str] = None,
        devices: Dict[str, Dict[str, str]] = None,
        ephemeral: bool = None,
        profiles: List[str] = None,
        stateful: bool = None,
        description: str = None,
        created_at: str = None,
        expanded_config: Dict[str, str] = None,
        expanded_devices: Dict[str, Dict[str, str]] = None,
        location: str = None,
        status: str = None,
        status_code: int = None,
        last_used_at: str = None,
        project: str = None,
        type: str = None,
        **kwargs,
    ):
        """
        Initialize a new Instance model.

        Args:
            client: The Incus client instance.
            name: Name of the instance.
            architecture: Architecture of the instance.
            config: Instance configuration.
            devices: Instance devices.
            ephemeral: Whether the instance is ephemeral.
            profiles: List of profiles applied to the instance.
            stateful: Whether the instance is stateful.
            description: Description of the instance.
            created_at: When the instance was created.
            expanded_config: Expanded configuration.
            expanded_devices: Expanded devices.
            location: Location of the instance.
            status: Current status of the instance.
            status_code: Current status code of the instance.
            last_used_at: When the instance was last used.
            project: Project the instance belongs to.
            type: Type of instance (container or virtual-machine).
            **kwargs: Additional attributes to set on the model.
        """
        self.name = name
        self.architecture = architecture
        self.config = config or {}
        self.devices = devices or {}
        self.ephemeral = ephemeral
        self.profiles = profiles or []
        self.stateful = stateful
        self.description = description
        self.created_at = created_at
        self.expanded_config = expanded_config or {}
        self.expanded_devices = expanded_devices or {}
        self.location = location
        self.status = status
        self.status_code = status_code
        self.last_used_at = last_used_at
        self.project = project
        self.type = type
        super().__init__(client=client, **kwargs)

    def __repr__(self):
        """Return a string representation of the instance."""
        return f"<Instance: {self.name}>"

    async def start(self, wait: bool = False) -> Dict[str, Any]:
        """
        Start the instance.

        Args:
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.start(self.name, wait=wait)

    async def stop(self, wait: bool = False, force: bool = False) -> Dict[str, Any]:
        """
        Stop the instance.

        Args:
            wait: Whether to wait for the operation to complete.
            force: Whether to force stop the instance.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.stop(self.name, wait=wait, force=force)

    async def restart(self, wait: bool = False, force: bool = False) -> Dict[str, Any]:
        """
        Restart the instance.

        Args:
            wait: Whether to wait for the operation to complete.
            force: Whether to force restart the instance.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.restart(self.name, wait=wait, force=force)

    async def delete(self, wait: bool = False) -> Dict[str, Any]:
        """
        Delete the instance.

        Args:
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.delete(self.name, wait=wait)

    async def update(
        self, config: Dict[str, Any], wait: bool = False
    ) -> Dict[str, Any]:
        """
        Update the instance configuration.

        Args:
            config: The new configuration.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.update(self.name, config, wait=wait)

    async def execute(
        self,
        command: List[str],
        environment: Dict[str, str] = None,
        wait_for_websocket: bool = False,
        record_output: bool = False,
        interactive: bool = False,
        width: int = None,
        height: int = None,
        user: int = None,
        group: int = None,
        cwd: str = None,
        wait: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute a command in the instance.

        Args:
            command: The command to execute.
            environment: Environment variables to set.
            wait_for_websocket: Whether to wait for a websocket connection.
            record_output: Whether to record the command output.
            interactive: Whether the command is interactive.
            width: Terminal width.
            height: Terminal height.
            user: User ID to run the command as.
            group: Group ID to run the command as.
            cwd: Working directory for the command.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        if not self._client:
            raise ValueError("No client available")

        return await self._client.instances.execute(
            self.name,
            command,
            environment=environment,
            wait_for_websocket=wait_for_websocket,
            record_output=record_output,
            interactive=interactive,
            width=width,
            height=height,
            user=user,
            group=group,
            cwd=cwd,
            wait=wait,
        )
