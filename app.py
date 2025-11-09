
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain import LLMChain

st.title("育児仕事用")
st.write("##### 動作モード1: 育児相談")
st.write("育児相談ができます。")
st.write("##### 動作モード2: プログラミング")
st.write("プログラミングの相談ができます。")

nutrition__template = """
あなたは親の育児の専門家です。
育児疲れやストレス管理に関する実践的なアドバイスを提供します。
親自身の心身の健康を保つための方法を教えます。
質問：{input}
"""

Programming_template = """
あなたはプログラミングアドバイザーです。
プログラミングに関する質問や相談に乗ります。
質問：{input}
"""

# LLMに回答を生成させる関数
def get_llm_response(input_text, selected_mode):
    from langchain.llms import OpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain
    
    # LLMのインスタンス作成
    llm = OpenAI(temperature=0.7)
    
    # 選択されたモードに応じてプロンプトテンプレートを選択
    if selected_mode == "育児相談":
        template = nutrition__template
    else:  # プログラミング
        template = Programming_template
    
    # プロンプトテンプレート作成
    prompt = PromptTemplate(
        input_variables=["input"],
        template=template
    )
    
    # チェーン作成
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # LLMから回答を取得
    response = chain.run(input=input_text)
    return response

selected_item = st.radio(
    "動作モードを選択してください。",
    ["育児相談", "プログラミング"]
)

st.divider()

# 入力フォーム
input_text = st.text_area(
    label="質問を入力してください。",
    placeholder="ここに質問を入力してください...",
    height=100
)

if st.button("実行"):
    st.divider()
    
    if input_text.strip():
        # LLMからの回答を取得して表示
        with st.spinner("回答を生成中..."):
            try:
                response = get_llm_response(input_text, selected_item)
                st.success("回答:")
                st.write(response)
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
    else:
        st.error("質問を入力してから「実行」ボタンを押してください。")