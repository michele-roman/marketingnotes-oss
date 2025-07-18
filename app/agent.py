# agent.py
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .models import Message, Chat, APIKey   
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_api_key(service):
    """Get API key from database for the specified service"""
    try:
        api_key_obj = APIKey.objects.get(service=service, is_active=True)
        return api_key_obj.api_key
    except APIKey.DoesNotExist:
        logger.warning(f"No active API key found for {service}")
        return None

def get_agent_response(chat_id=None):
    """Legacy function - now returns OpenAI agent for backward compatibility"""
    return get_openai_agent(chat_id)

def get_openai_agent(chat_id=None):
    """Get OpenAI agent response function"""
    logger.info(f"\n=== OPENAI AGENT RESPONSE CALLED ===\n")
    logger.info(f"Chat ID: {chat_id}")
    
    # Get API key from database
    openai_api_key = get_api_key('openai')
    if not openai_api_key:
        logger.error("OpenAI API key not found or not active")
        return lambda message: "OpenAI API key not configured. Please add your API key in the settings."
    
    # Get chat history if chat_id is provided
    chat_messages = []
    if chat_id:
        logger.info(f"\n=== RETRIEVING CHAT HISTORY FOR CHAT ID: {chat_id} ===\n")
        try:
            messages = Message.objects.filter(chat_id=chat_id).order_by('date')
            logger.info(f"Query executed. Messages found: {messages.count()}")
            
            if messages.exists():
                for msg in messages:
                    logger.info(f"Found message - ID: {msg.id}, Sender: {msg.sender}, Content: {msg.content}, Date: {msg.date}")
                    if msg.sender == "user":
                        chat_messages.append(HumanMessage(content=msg.content))
                    else:
                        chat_messages.append(AIMessage(content=msg.content))
                logger.info(f"Total messages processed: {len(chat_messages)}\n")
            else:
                logger.info("No messages found in the database for this chat_id")
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
        logger.info("===========================================\n")

    # Dynamic mentor prompt
    mentor_prompt = f"""
    You are an expert in marketing and sales, specializing in content creation, email message generation, article writing, and other marketing communications.

    Your task is to create compelling, persuasive, and effective marketing content that drives engagement, conversions, and sales results.

    CRITICAL RULES:
    1. ALWAYS check the conversation history before responding
    2. NEVER ask for information that has already been provided in the conversation
    3. If information exists in the conversation history, you MUST use it
    4. If asked about previously mentioned information, you MUST reference it correctly
    5. NEVER invent or assume information about the business that hasn't been explicitly mentioned
    6. If you're unsure about any business details, ask for clarification instead of making assumptions
    7. If you notice any inconsistency in your previous responses, acknowledge and correct it
    8. ALWAYS use the specific attribute data provided above when giving advice or creating content
    9. ALWAYS divide your answers into different and distinct paragraphs for better readability and structure
    
    Additional guidelines:
    - Consider the context from previous messages to maintain continuity
    - Maintain a professional and motivating tone
    - Each message must be aligned with the user's question
    - **Limit the length of your responses** to be clear and concise by default — **unless the user specifically asks for more depth, longer formats, or multiple versions**  
    - When using bullet points or lists, do NOT exceed 6 items unless explicitly requested
    """

    llm = ChatOpenAI(
        model="gpt-4o",  # Using GPT-4 Turbo
        openai_api_key=openai_api_key,
        temperature=0.7,
        max_tokens=500  # Limiting response length to ensure concise answers
    )

    def ask(message):
        # Create a summary of the conversation context
        context_summary = "IMPORTANT - CONVERSATION CONTEXT:\n"
        if chat_messages:
            context_summary += "Previous messages in this conversation (MUST BE USED):\n"
            for msg in chat_messages:  # Include all messages for complete context
                if isinstance(msg, HumanMessage):
                    context_summary += f"User: {msg.content}\n"
                else:
                    context_summary += f"Assistant: {msg.content}\n"
            context_summary += "\nREMEMBER: Do not ask for information that has already been provided in these messages. Always reference previous information when relevant."

        # Log the chat messages for debugging
        logger.info("\n=== CHAT HISTORY ===\n")
        for msg in chat_messages:
            if isinstance(msg, HumanMessage):
                logger.info(f"Previous User Message: {msg.content}")
            else:
                logger.info(f"Previous Assistant Message: {msg.content}")
        logger.info("===================\n")

        messages = [
            SystemMessage(content=mentor_prompt),
            SystemMessage(content=context_summary)
        ]
        
        # Add chat history as actual conversation messages
        if chat_messages:
            messages.extend(chat_messages)
        
        # Add the current message
        messages.append(HumanMessage(content=message))
        
        # Log all messages being sent to OpenAI
        logger.info("\n=== MESSAGES BEING SENT TO OPENAI ===\n")
        for msg in messages:
            if isinstance(msg, SystemMessage):
                logger.info(f"System Message:\n{msg.content}\n")
            elif isinstance(msg, HumanMessage):
                logger.info(f"Human Message:\n{msg.content}\n")
            elif isinstance(msg, AIMessage):
                logger.info(f"AI Message:\n{msg.content}\n")
        logger.info("=====================================\n")
        
        response = llm(messages)
        return response.content

    return ask

def get_gemini_agent(chat_id=None):
    """Get Gemini agent response function"""
    logger.info(f"\n=== GEMINI AGENT RESPONSE CALLED ===\n")
    logger.info(f"Chat ID: {chat_id}")
    
    # Get API key from database
    gemini_api_key = get_api_key('gemini')
    if not gemini_api_key:
        logger.error("Gemini API key not found or not active")
        return lambda message: "Gemini API key not configured. Please add your API key in the settings."
    
    # Get chat history if chat_id is provided
    chat_messages = []
    if chat_id:
        logger.info(f"\n=== RETRIEVING CHAT HISTORY FOR CHAT ID: {chat_id} ===\n")
        try:
            messages = Message.objects.filter(chat_id=chat_id).order_by('date')
            logger.info(f"Query executed. Messages found: {messages.count()}")
            
            if messages.exists():
                for msg in messages:
                    logger.info(f"Found message - ID: {msg.id}, Sender: {msg.sender}, Content: {msg.content}, Date: {msg.date}")
                    if msg.sender == "user":
                        chat_messages.append(HumanMessage(content=msg.content))
                    else:
                        chat_messages.append(AIMessage(content=msg.content))
                logger.info(f"Total messages processed: {len(chat_messages)}\n")
            else:
                logger.info("No messages found in the database for this chat_id")
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
        logger.info("===========================================\n")

    # Dynamic mentor prompt with attribute data (same as OpenAI for consistency)
    mentor_prompt = f"""
    You are an expert in marketing and sales, specializing in content creation, email message generation, article writing, and other marketing communications.

    Your task is to create compelling, persuasive, and effective marketing content that drives engagement, conversions, and sales results.

    CRITICAL RULES:
    1. ALWAYS check the conversation history before responding
    2. NEVER ask for information that has already been provided in the conversation
    3. If information exists in the conversation history, you MUST use it
    4. If asked about previously mentioned information, you MUST reference it correctly
    5. NEVER invent or assume information about the business that hasn't been explicitly mentioned
    6. If you're unsure about any business details, ask for clarification instead of making assumptions
    7. If you notice any inconsistency in your previous responses, acknowledge and correct it
    8. ALWAYS use the specific attribute data provided above when giving advice or creating content
    9. ALWAYS divide your answers into different and distinct paragraphs for better readability and structure
    
    Additional guidelines:
    - Consider the context from previous messages to maintain continuity
    - Maintain a professional and motivating tone
    - Each message must be aligned with the user's question
    - **Limit the length of your responses** to be clear and concise by default — **unless the user specifically asks for more depth, longer formats, or multiple versions**  
    - When using bullet points or lists, do NOT exceed 6 items unless explicitly requested
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=gemini_api_key,
        temperature=0.7,
        max_output_tokens=500  # Limiting response length to ensure concise answers
    )

    def ask(message):
        # Create a summary of the conversation context
        context_summary = "IMPORTANT - CONVERSATION CONTEXT:\n"
        if chat_messages:
            context_summary += "Previous messages in this conversation (MUST BE USED):\n"
            for msg in chat_messages:  # Include all messages for complete context
                if isinstance(msg, HumanMessage):
                    context_summary += f"User: {msg.content}\n"
                else:
                    context_summary += f"Assistant: {msg.content}\n"
            context_summary += "\nREMEMBER: Do not ask for information that has already been provided in these messages. Always reference previous information when relevant."

        # Log the chat messages for debugging
        logger.info("\n=== CHAT HISTORY ===\n")
        for msg in chat_messages:
            if isinstance(msg, HumanMessage):
                logger.info(f"Previous User Message: {msg.content}")
            else:
                logger.info(f"Previous Assistant Message: {msg.content}")
        logger.info("===================\n")

        messages = [
            SystemMessage(content=mentor_prompt),
            SystemMessage(content=context_summary)
        ]
        
        # Add chat history as actual conversation messages
        if chat_messages:
            messages.extend(chat_messages)
        
        # Add the current message
        messages.append(HumanMessage(content=message))
        
        # Log all messages being sent to Gemini
        logger.info("\n=== MESSAGES BEING SENT TO GEMINI ===\n")
        for msg in messages:
            if isinstance(msg, SystemMessage):
                logger.info(f"System Message:\n{msg.content}\n")
            elif isinstance(msg, HumanMessage):
                logger.info(f"Human Message:\n{msg.content}\n")
            elif isinstance(msg, AIMessage):
                logger.info(f"AI Message:\n{msg.content}\n")
        logger.info("=====================================\n")
        
        response = llm(messages)
        return response.content

    return ask

def get_antropic_agent(chat_id=None):
    """Get Antropic (Claude) agent response function"""
    logger.info(f"\n=== ANTROPIC AGENT RESPONSE CALLED ===\n")
    logger.info(f"Chat ID: {chat_id}")
    
    # Get API key from database
    anthropic_api_key = get_api_key('anthropic')
    if not anthropic_api_key:
        logger.error("Anthropic API key not found or not active")
        return lambda message: "Anthropic API key not configured. Please add your API key in the settings."
    
    # Get chat history if chat_id is provided
    chat_messages = []
    if chat_id:
        logger.info(f"\n=== RETRIEVING CHAT HISTORY FOR CHAT ID: {chat_id} ===\n")
        try:
            messages = Message.objects.filter(chat_id=chat_id).order_by('date')
            logger.info(f"Query executed. Messages found: {messages.count()}")
            
            if messages.exists():
                for msg in messages:
                    logger.info(f"Found message - ID: {msg.id}, Sender: {msg.sender}, Content: {msg.content}, Date: {msg.date}")
                    if msg.sender == "user":
                        chat_messages.append(HumanMessage(content=msg.content))
                    else:
                        chat_messages.append(AIMessage(content=msg.content))
                logger.info(f"Total messages processed: {len(chat_messages)}\n")
            else:
                logger.info("No messages found in the database for this chat_id")
        except Exception as e:
            logger.error(f"Error retrieving chat history: {str(e)}")
        logger.info("===========================================\n")

    # Dynamic mentor prompt with attribute data (same as OpenAI for consistency)
    mentor_prompt = f"""
    You are an expert in marketing and sales, specializing in content creation, email message generation, article writing, and other marketing communications.

    Your task is to create compelling, persuasive, and effective marketing content that drives engagement, conversions, and sales results.

    CRITICAL RULES:
    1. ALWAYS check the conversation history before responding
    2. NEVER ask for information that has already been provided in the conversation
    3. If information exists in the conversation history, you MUST use it
    4. If asked about previously mentioned information, you MUST reference it correctly
    5. NEVER invent or assume information about the business that hasn't been explicitly mentioned
    6. If you're unsure about any business details, ask for clarification instead of making assumptions
    7. If you notice any inconsistency in your previous responses, acknowledge and correct it
    8. ALWAYS use the specific attribute data provided above when giving advice or creating content
    9. ALWAYS divide your answers into different and distinct paragraphs for better readability and structure
    
    Additional guidelines:
    - Consider the context from previous messages to maintain continuity
    - Maintain a professional and motivating tone
    - Each message must be aligned with the user's question
    - **Limit the length of your responses** to be clear and concise by default — **unless the user specifically asks for more depth, longer formats, or multiple versions**  
    - When using bullet points or lists, do NOT exceed 6 items unless explicitly requested
    """

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022",
        anthropic_api_key=anthropic_api_key,
        temperature=0.7,
        max_tokens=500  # Limiting response length to ensure concise answers
    )

    def ask(message):
        # Create a summary of the conversation context
        context_summary = "IMPORTANT - CONVERSATION CONTEXT:\n"
        if chat_messages:
            context_summary += "Previous messages in this conversation (MUST BE USED):\n"
            for msg in chat_messages:  # Include all messages for complete context
                if isinstance(msg, HumanMessage):
                    context_summary += f"User: {msg.content}\n"
                else:
                    context_summary += f"Assistant: {msg.content}\n"
            context_summary += "\nREMEMBER: Do not ask for information that has already been provided in these messages. Always reference previous information when relevant."

        # Log the chat messages for debugging
        logger.info("\n=== CHAT HISTORY ===\n")
        for msg in chat_messages:
            if isinstance(msg, HumanMessage):
                logger.info(f"Previous User Message: {msg.content}")
            else:
                logger.info(f"Previous Assistant Message: {msg.content}")
        logger.info("===================\n")

        messages = [
            SystemMessage(content=mentor_prompt),
            SystemMessage(content=context_summary)
        ]
        
        # Add chat history as actual conversation messages
        if chat_messages:
            messages.extend(chat_messages)
        
        # Add the current message
        messages.append(HumanMessage(content=message))
        
        # Log all messages being sent to Anthropic
        logger.info("\n=== MESSAGES BEING SENT TO ANTHROPIC ===\n")
        for msg in messages:
            if isinstance(msg, SystemMessage):
                logger.info(f"System Message:\n{msg.content}\n")
            elif isinstance(msg, HumanMessage):
                logger.info(f"Human Message:\n{msg.content}\n")
            elif isinstance(msg, AIMessage):
                logger.info(f"AI Message:\n{msg.content}\n")
        logger.info("=====================================\n")
        
        response = llm(messages)
        return response.content

    return ask

def get_custom_agent(chat_id=None):
    """Get custom agent response function"""
    logger.info(f"\n=== CUSTOM AGENT RESPONSE CALLED ===\n")
    logger.info(f"Chat ID: {chat_id}")
    
    def ask(message):
        # For the custom agent, we return a special response that triggers the editor
        # The actual response will be built by the user through the UI
        
        custom_response = f"""
        """
        
        return custom_response

    return ask