
from configuration import BOT_CONFIG, Message
from .database import (get_async_session, get_chat)

from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from llm_memory import (
    CustomConversationBufferWindowMemory as ConversationBufferWindowMemory)
from llm_memory import CustomRedisChatMessageHistory as RedisChatMessageHistory


redis_message_history = RedisChatMessageHistory(session_id='',
                                                ttl=100,
                                                max_len=BOT_CONFIG.LLM_MAX_LEN,
                                                url="redis://default:sOCRmwFmixOsQPR0ai7OLHO90oPHNxGO@redis-13097.c114.us-east-1-4.ec2.cloud.redislabs.com:13097")


def remove_prefix(s, prefix):
    return s[len(prefix):]


def chain_setup():
    template = BOT_CONFIG.DEFAULT_PREFIX + \
        """\n\n{chat_history}\n<|prompter|>{question}<|endoftext|><|assistant|>"""
    prompt = PromptTemplate(template=template, input_variables=[
                            "chat_history", "question"])

    memory = ConversationBufferWindowMemory(memory_key="chat_history")
    llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5",
                         model_kwargs={"max_new_tokens": 1200, "temperature": 0.4})
    llm_chain = LLMChain(
        llm=llm,
        verbose=True,
        prompt=prompt,
        memory=memory,
    )
    return llm_chain


def generate_response(chat_id: int,
                      question: Message):
    redis_message_history.session_id = str(chat_id)
    messages = redis_message_history.messages
    llm_chain.memory.chat_memory.messages = messages

    # question = translator.translate(text=question, src='ru', dest='en').text
    print(f'\nquestion: {question}')
    # print(f'\nprefix: {prefix}')
    print(f'\nmessages: {messages}')
    response = llm_chain.predict(question=question.get(BOT_CONFIG.LLM_LANG))
    print(f'\n response: {response}')
    result = Message(message=response, default_lang=BOT_CONFIG.LLM_LANG)
    # translation = translator.translate(text=response, src='en', dest='ru').text
    redis_message_history.add_message(messages[-2])
    redis_message_history.add_message(messages[-1])

    return result


async def get_prefix(chat_id: int, default_lang: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)
    return chat.prefix


async def set_prefix(chat_id: int,
                     default_lang: str,
                     arg: str):
    session = await get_async_session()
    chat = await get_chat(chat_id=chat_id, lang=default_lang, session=session)

    chat.prefix = arg
    await session.merge(chat)
    await session.commit()
    return BOT_CONFIG.SUCCESS_RESULT_MESSAGE.get(chat.language)


llm_chain = chain_setup()
