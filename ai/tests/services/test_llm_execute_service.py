"""
Test cases for LLMExecuteService using mocks from conftest.py
"""

from unittest.mock import Mock, patch

from ai.model.workflow import WorkflowNodeRequest
from ai.services.llm_service.llm_execute_service import LLMExecuteService


def test_llm_execute_service_with_mock_fixture(mock_llm_execute_service):
    """
    Test using the mock fixture directly (for testing external code that uses the service)
    """
    exec_id = "test-exec-id"
    node = WorkflowNodeRequest(
        name="test-node", type="LLM", message="Test message", prompt="Test prompt"
    )

    # Use the mock service directly
    mock_llm_execute_service.execute(exec_id, node)

    # Verify the method was called
    mock_llm_execute_service.execute.assert_called_once_with(exec_id, node)


def test_llm_execute_service_execute_llm_with_dependencies_mocked():
    """
    Test the actual LLMExecuteService by mocking its dependencies
    """
    exec_id = "test-exec-id"
    node = WorkflowNodeRequest(
        name="test-node",
        type="LLM",
        message="Test message",
        prompt="Test prompt",
        llm="OpenAI",
    )

    # Mock the dependencies at the right path within the service module
    with patch(
        "ai.services.llm_service.llm_execute_service.LlmService"
    ) as mock_llm_service, patch(
        "ai.services.llm_service.llm_execute_service.AiMessageManager"
    ) as mock_ai_message_manager:

        # Setup the mocks
        mock_llm = Mock()
        mock_llm.invoke.return_value = Mock(
            id="test-id",
            content="Test response",
            response_metadata={"model_name": "test-model"},
        )
        mock_llm_service.return_value.get_llm.return_value = mock_llm
        mock_ai_message_manager.return_value.save_data.return_value = None

        # Create the actual service and test it
        service = LLMExecuteService()
        service.execute_llm(exec_id, node)

        # Verify dependencies were called
        from ai.model.enums import LLMs

        mock_llm_service.return_value.get_llm.assert_called_once_with(
            llm=LLMs.OpenAI, structured_output=None
        )
        mock_ai_message_manager.return_value.save_data.assert_called_once()


def test_llm_execute_service_execute_agent_with_dependencies_mocked():
    """
    Test the agent execution path with mocked dependencies
    """
    exec_id = "test-exec-id"
    node = WorkflowNodeRequest(
        name="test-node",
        type="Agent",
        message="Test message",
        prompt="Test prompt",
        llm="OpenAI",
        tools=[],
    )

    # Mock all the dependencies at the right path within the service module
    with patch(
        "ai.services.llm_service.llm_execute_service.LlmService"
    ) as mock_llm_service, patch(
        "ai.services.llm_service.llm_execute_service.AiMessageManager"
    ) as mock_ai_message_manager, patch(
        "ai.services.llm_service.llm_execute_service.create_react_agent"
    ) as mock_create_agent, patch(
        "ai.services.llm_service.llm_execute_service.ToolService"
    ) as mock_tool_service:

        # Setup all the mocks
        mock_llm = Mock()
        mock_llm_service.return_value.get_llm.return_value = mock_llm
        mock_ai_message_manager.return_value.save_data.return_value = None
        mock_tool_service.return_value.get_tool_func.return_value = Mock()

        mock_agent = Mock()
        mock_agent.stream.return_value = [
            {"messages": [Mock(content="Agent response")]}
        ]
        mock_create_agent.return_value = mock_agent

        # Test the service
        service = LLMExecuteService()
        service.execute_agent(exec_id, node)

        # Verify calls
        mock_llm_service.return_value.get_llm.assert_called_once()
        mock_create_agent.assert_called_once()
        mock_ai_message_manager.return_value.save_data.assert_called_once()


@patch("ai.services.llm_service.llm_execute_service.LLMExecuteService")
def test_llm_execute_service_with_complete_patch(mock_service_class):
    """
    Test using manual patching with @patch decorator (for integration tests)
    """
    # Configure the mock
    mock_instance = mock_service_class.return_value
    mock_instance.execute.return_value = None

    exec_id = "test-exec-id"
    node = WorkflowNodeRequest(
        name="test-node", type="LLM", message="Test message", prompt="Test prompt"
    )

    # Import and use the service (will use the mock)
    from ai.services.llm_service.llm_execute_service import LLMExecuteService

    service = LLMExecuteService()
    service.execute(exec_id, node)

    # Verify
    mock_service_class.assert_called_once()
    mock_instance.execute.assert_called_once_with(exec_id, node)


def test_llm_execute_service_execute_method_routing():
    """
    Test that the execute method correctly routes to LLM or Agent execution
    """
    with patch.object(
        LLMExecuteService, "execute_llm"
    ) as mock_execute_llm, patch.object(
        LLMExecuteService, "execute_agent"
    ) as mock_execute_agent:

        service = LLMExecuteService()
        exec_id = "test-exec-id"

        # Test LLM routing
        llm_node = WorkflowNodeRequest(
            name="llm-node", type="LLM", message="Test message"
        )
        service.execute(exec_id, llm_node)
        mock_execute_llm.assert_called_once_with(exec_id, llm_node)

        # Test Agent routing
        agent_node = WorkflowNodeRequest(
            name="agent-node", type="Agent", message="Test message"
        )
        service.execute(exec_id, agent_node)
        mock_execute_agent.assert_called_once_with(exec_id, agent_node)
