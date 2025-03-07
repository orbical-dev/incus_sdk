"""
Instances API client for Incus API.
"""

from typing import Dict, Any, List, Union

from incus_sdk.api.client import APIClient
from incus_sdk.models.instance import Instance


class InstancesAPI:
    """API client for Incus instances."""

    def __init__(self, client: APIClient):
        """
        Initialize a new InstancesAPI client.

        Args:
            client: The base API client.
        """
        self.client = client

    async def list(self, recursion: int = 1) -> List[Instance]:
        """
        List all instances.

        Args:
            recursion: Level of recursion for the response.

        Returns:
            List[Instance]: List of instances.
        """
        params = {"recursion": recursion}
        response = await self.client.get("/1.0/instances", params=params)

        instances = []
        for instance_data in response.get("metadata", []):
            instances.append(Instance(client=self, **instance_data))

        return instances

    async def get(self, name: str) -> Instance:
        """
        Get an instance by name.

        Args:
            name: Name of the instance.

        Returns:
            Instance: The instance.
        """
        response = await self.client.get(
            f"/1.0/instances/{name}"
        )
        return Instance(client=self, **response.get("metadata", {}))

    async def create(
        self,
        name: str,
        source: Dict[str, Any],
        config: Dict[str, Any] = None,
        devices: Dict[str, Dict[str, Any]] = None,
        profiles: List[str] = None,
        ephemeral: bool = False,
        instance_type: str = "container",
        wait: bool = False,
    ) -> Union[Dict[str, Any], Instance]:
        """
        Create a new instance.

        Args:
            name: Name of the instance.
            source: Source configuration for the instance.
            config: Instance configuration.
            devices: Instance devices.
            profiles: List of profiles to apply.
            ephemeral: Whether the instance is ephemeral.
            instance_type: Type of instance (container or virtual-machine).
            wait: Whether to wait for the operation to complete.

        Returns:
            Union[Dict[str, Any], Instance]: The operation response or the created
            instance.
        """
        data = {"name": name, "source": source, "type": instance_type}

        if config:
            data["config"] = config
        if devices:
            data["devices"] = devices
        if profiles:
            data["profiles"] = profiles
        if ephemeral:
            data["ephemeral"] = ephemeral

        response = await self.client.post("/1.0/instances", data=data)

        if wait and "id" in response.get("metadata", {}):
            await self.client.wait_for_operation(response["metadata"]["id"])
            return await self.get(name)

        return response

    async def update(
        self, name: str, config: Dict[str, Any], wait: bool = False
    ) -> Dict[str, Any]:
        """
        Update an instance.

        Args:
            name: Name of the instance.
            config: New configuration.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        response = await self.client.put(f"/1.0/instances/{name}", data=config)

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(
                response["metadata"]["id"]
            )

        return response

    async def delete(self, name: str, wait: bool = False) -> Dict[str, Any]:
        """
        Delete an instance.

        Args:
            name: Name of the instance.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        response = await self.client.delete(f"/1.0/instances/{name}")

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(
                response["metadata"]["id"]
            )

        return response

    async def _state_action(
        self,
        name: str,
        action: str,
        force: bool = False,
        stateful: bool = False,
        timeout: int = 30,
        wait: bool = False,
    ) -> Dict[str, Any]:
        """
        Perform a state action on an instance.

        Args:
            name: Name of the instance.
            action: Action to perform (start, stop, restart, freeze, unfreeze).
            force: Whether to force the action.
            stateful: Whether to preserve the instance state.
            timeout: Timeout in seconds.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        data = {
            "action": action,
            "force": force,
            "stateful": stateful,
            "timeout": timeout,
        }

        response = await self.client.put(
            f"/1.0/instances/{name}/state", data=data
        )

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(
                response["metadata"]["id"]
            )

        return response

    async def start(
        self, name: str, stateful: bool = False, wait: bool = False
    ) -> Dict[str, Any]:
        """
        Start an instance.

        Args:
            name: Name of the instance.
            stateful: Whether to restore state.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self._state_action(name, "start", stateful=stateful, wait=wait)

    async def stop(
        self,
        name: str,
        force: bool = False,
        stateful: bool = False,
        wait: bool = False
    ) -> Dict[str, Any]:
        """
        Stop an instance.

        Args:
            name: Name of the instance.
            force: Whether to force stop.
            stateful: Whether to preserve state.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self._state_action(
            name, "stop", force=force, stateful=stateful, wait=wait
        )

    async def restart(
        self, name: str, force: bool = False, wait: bool = False
    ) -> Dict[str, Any]:
        """
        Restart an instance.

        Args:
            name: Name of the instance.
            force: Whether to force restart.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self._state_action(name, "restart", force=force, wait=wait)

    async def freeze(self, name: str, wait: bool = False) -> Dict[str, Any]:
        """
        Freeze an instance.

        Args:
            name: Name of the instance.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self._state_action(name, "freeze", wait=wait)

    async def unfreeze(self, name: str, wait: bool = False) -> Dict[str, Any]:
        """
        Unfreeze an instance.

        Args:
            name: Name of the instance.
            wait: Whether to wait for the operation to complete.

        Returns:
            Dict[str, Any]: The operation response.
        """
        return await self._state_action(name, "unfreeze", wait=wait)

    async def execute(
        self,
        name: str,
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
        Execute a command in an instance.

        Args:
            name: Name of the instance.
            command: Command to execute.
            environment: Environment variables.
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
        data = {
            "command": command,
            "wait-for-websocket": wait_for_websocket,
            "record-output": record_output,
            "interactive": interactive,
        }

        if environment:
            data["environment"] = environment
        if width:
            data["width"] = width
        if height:
            data["height"] = height
        if user:
            data["user"] = user
        if group:
            data["group"] = group
        if cwd:
            data["cwd"] = cwd

        response = await self.client.post(
            f"/1.0/instances/{name}/exec", data=data
        )

        if wait and "id" in response.get("metadata", {}):
            return await self.client.wait_for_operation(
                response["metadata"]["id"]
            )

        return response
