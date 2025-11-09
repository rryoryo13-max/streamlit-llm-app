from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()


def get_llm_response(input_text: str, expert_type: str) -> str:
    """
    LLMに入力テキストを送信し、専門家として回答を取得する関数
    
    Args:
        input_text (str): ユーザーからの質問テキスト
        expert_type (str): 専門家の種類（"調理の専門家" または "育児の専門家"）
    
    Returns:
        str: LLMからの回答
    """
    # 専門家の種類に応じてシステムメッセージを設定
    if expert_type == "調理の専門家":
        system_message = "あなたは調理と料理に関する専門家です。料理のレシピ、調理法、食材に関する質問に詳しく丁寧に答えてください。"
    else:  # 育児の専門家
        system_message = "あなたは育児と子育てに関する専門家です。子供の成長、しつけ、育児の悩みに関する質問に詳しく丁寧に答えてください。"
    
    # LLMの初期化
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    # メッセージの作成
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text)
    ]
    
    # LLMからの応答を取得
    try:
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


st.title("専門家AI相談アプリ")

st.write("##### アプリの概要")
st.write("このアプリでは、調理または育児の専門家として振る舞うAIに質問することができます。")
st.write("##### 操作方法")
st.write("1. 専門家の種類をラジオボタンで選択してください")
st.write("2. 質問したい内容をテキストフォームに入力してください") 
st.write("3. 「回答を取得」ボタンを押すと、AIからの回答が表示されます")

st.divider()

# 専門家の種類を選択
expert_type = st.radio(
    "相談したい専門家を選択してください:",
    ["調理の専門家", "育児の専門家"]
)

# 質問テキストの入力
user_question = st.text_area(
    label="質問を入力してください:",
    placeholder="例: 簡単にできる夕食のレシピを教えて",
    height=100
)

# 回答取得ボタン
if st.button("回答を取得"):
    if user_question.strip():
        st.divider()
        
        with st.spinner("AIが回答を生成中..."):
            response = get_llm_response(user_question, expert_type)
        
        st.write("##### AI専門家からの回答:")
        st.write(response)
    else:
        st.error("質問を入力してから「回答を取得」ボタンを押してください。")