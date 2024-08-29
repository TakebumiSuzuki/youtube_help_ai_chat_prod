import ui_constants as UC
import conversation_logic as logic
import streamlit as st
import uuid
import time # Gemini使用でストリームする場合のみ使う
import random # Gemini使用でストリームする場合のみ使う

MAX_USER_INPUT = 200
LANG = 'language'
CONV = 'conversation'
CURRENT_DOCS = 'current_docs'
DOCS_STORE = 'docs_store'
SHOW_CLEAR_BUTTON = 'show_clear_button'

ss = st.session_state

if CONV not in ss:
    ss[CONV] = []
message_list = ss[CONV]

if DOCS_STORE not in ss:
    ss[DOCS_STORE] = {}

if CURRENT_DOCS not in ss:
    ss[CURRENT_DOCS] = ""

if SHOW_CLEAR_BUTTON not in ss:
    ss[SHOW_CLEAR_BUTTON] = False

if LANG not in ss:
    ss[LANG] = UC.ENGLISH

st.set_page_config(
     page_title = UC.TAB_TITLE(ss[LANG]),
     layout = "wide",
     initial_sidebar_state = "expanded"
)

# unsafe_allow_html=True を使用して、HTMLとCSSの直接挿入を許可
st.markdown(UC.CSS, unsafe_allow_html=True)

st.title(UC.TITLE(ss[LANG]))
st.write(UC.SUBTITLE(ss[LANG]))

# Display chat messages from history on app rerun
if message_list != []:
    for message in message_list:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "AI":
                if st.button(UC.DOC_HISTORY(ss[LANG]), key = message["key"]):
                    ss[CURRENT_DOCS] = ss[DOCS_STORE][message["key"]]

    if ss[SHOW_CLEAR_BUTTON] == True:
        clear_button = st.button(UC.CLEAR_BUTTON(ss[LANG]))
        if clear_button == True:
            ss[CONV] = []
            ss[CURRENT_DOCS] = ""
            clear_button = False
            st.rerun()

def hide_clear_button():
    ss[SHOW_CLEAR_BUTTON] = False

# Accept user input
if input := st.chat_input(UC.INPUT_HOLDER(ss[LANG]), on_submit = hide_clear_button):
    # インプとの文字数のモデレート
    if len(input) > MAX_USER_INPUT:
        input = input[:MAX_USER_INPUT]
    #ユーザーからのインプットをそのままUIに表示する
    with st.chat_message("user"):
        st.markdown(input)
    #ユーザーからのインプットをsession_stateに記録
    ss[CONV].append({"role" : "user", "content" : input})

    #AIからの返答をストリームにて取得、表示する
    with st.chat_message("AI"):
        msg_holder = st.empty()
        msg_holder.markdown("Searching...")

        sources, language = logic.handle_retrieval(input)
        ss[CURRENT_DOCS] = sources
        ss[LANG] = language
        print(ss[LANG])

        with st.sidebar:
            st.subheader(UC.SIDEBAR_SUBTITLE(ss[LANG]))

            if CURRENT_DOCS in ss:
                st.markdown(ss[CURRENT_DOCS])

        msg_holder.markdown("Reading source documents...")
        full_response = ""
        stream = logic.get_stream(input, sources, ss[LANG])
        for chunk in stream:
            try:
                # Geminiの場合
                word_count = 0
                random_int = random.randint(5, 10)
                for word in chunk.text:
                    full_response += word
                    word_count += 1
                    if word_count == random_int:
                        msg_holder.markdown(full_response + "_")
                        time.sleep(0.02)
                        word_count = 0
                        random_int = random.randint(5, 10)

            except Exception as e:
                print('AIからの回答を記述中に不明のエラーが発生しました: f{e}')
                raise

        msg_holder.markdown(full_response)


    # AIからの返答をsession_stateに記録
    generated_key = uuid.uuid4()
    ss[CONV].append({"role" : "AI", "content" : full_response, "key" : generated_key})
    ss[DOCS_STORE][generated_key] = sources
    ss[SHOW_CLEAR_BUTTON] = True
    st.rerun()

else:
    with st.sidebar:
        st.subheader(UC.SIDEBAR_SUBTITLE(ss[LANG]))
        if CURRENT_DOCS in ss:
            st.markdown(ss[CURRENT_DOCS])






