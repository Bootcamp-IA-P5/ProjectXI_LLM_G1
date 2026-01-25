- He añadido groq_client en api.py para pasar los test(No existía variable).
- He modificado api_test para codigo 500.
- Falta que Kas nos explique que pasa con sus tests.
Logs: 
FAILED tests/test_groq_agent.py::TestLLMFactoryUnit::test_llm_factory_missing_api_key - ModuleNotFoundError: No module named 'langchain_groq'
FAILED tests/test_groq_agent.py::TestLLMFactoryUnit::test_llm_factory_creates_groq_client_with_correct_params - ModuleNotFoundError: No module named 'langchain_groq'
FAILED tests/test_groq_agent.py::TestLLMFactoryUnit::test_llm_factory_uses_default_groq_params - ModuleNotFoundError: No module named 'langchain_groq'
FAILED tests/test_groq_agent.py::TestLLMFactoryUnit::test_llm_factory_default_provider - ModuleNotFoundError: No module named 'langchain_groq'
FAILED tests/test_groq_agent.py::TestLLMFactoryIntegration::test_llm_factory_groq_client_creation - Failed: Failed to create Groq client: No module named 'langchain_groq'
FAILED tests/test_groq_agent.py::TestLLMFactoryIntegration::test_llm_factory_groq_with_custom_model - Failed: Failed to create Groq client with custom model: No module named 'langchain_groq'