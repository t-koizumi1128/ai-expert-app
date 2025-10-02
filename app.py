import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Expert Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI エキスパート アシスタント")
st.markdown("専門家AIがあなたの質問に答えます")

st.sidebar.header("⚙️ 設定")
st.sidebar.info("""
### 使い方
1. 専門家を選択
2. 質問を入力  
3. 送信ボタンをクリック
""")

EXPERTS = {
    "💼 ビジネスコンサルタント": {
        "system": "経験豊富なビジネスコンサルタントとして、戦略立案、マーケティング、組織運営について実践的なアドバイスを提供してください。",
        "placeholder": "例: スタートアップの資金調達戦略について"
    },
    "💻 ITエンジニア": {
        "system": "熟練のITエンジニアとして、プログラミング、システム設計、最新技術についてコード例を含めて説明してください。",
        "placeholder": "例: Pythonでの効率的なAPI設計について"
    },
    "🏥 健康アドバイザー": {
        "system": "健康とウェルネスの専門家として、栄養、運動、メンタルヘルスについて科学的根拠に基づいたアドバイスを提供してください。",
        "placeholder": "例: デスクワークでの健康管理方法"
    },
    "📚 教育スペシャリスト": {
        "system": "教育の専門家として、効果的な学習方法、カリキュラム設計について分かりやすく説明してください。",
        "placeholder": "例: AIプログラミングの学習ロードマップ"
    },
    "🎨 クリエイティブディレクター": {
        "system": "クリエイティブディレクターとして、デザイン、ブランディング、コンテンツ制作について革新的なアイデアを提供してください。",
        "placeholder": "例: Z世代向けのマーケティング戦略"
    }
}

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("⚠️ OpenAI APIキーが設定されていません。")
    st.info("環境変数またはStreamlit Secretsに設定してください。")
    st.stop()

@st.cache_data(show_spinner=False)
def get_expert_response(question, expert_type):
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=1500,
            api_key=api_key
        )
        
        messages = [
            SystemMessage(content=EXPERTS[expert_type]["system"]),
            HumanMessage(content=question)
        ]
        
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎯 専門家を選択")
    selected_expert = st.radio(
        "相談したい専門家:",
        list(EXPERTS.keys()),
        index=0
    )
    
    with st.expander("詳細設定"):
        temperature = st.slider(
            "創造性レベル",
            0.0, 1.0, 0.7,
            help="0に近いほど一貫性が高く、1に近いほど創造的"
        )

with col2:
    st.subheader("💬 質問を入力")
    user_question = st.text_area(
        "質問内容:",
        height=150,
        placeholder=EXPERTS[selected_expert]["placeholder"]
    )
    
    if st.button("🚀 送信", type="primary"):
        if user_question:
            with st.spinner(f"{selected_expert}が回答を作成中..."):
                response = get_expert_response(user_question, selected_expert)
            
            st.markdown("---")
            st.subheader(f"📝 {selected_expert}からの回答")
            st.markdown(response)
            
            st.text_area("コピー用:", response, height=100)
        else:
            st.warning("質問を入力してください。")

st.markdown("---")
st.caption("Powered by OpenAI GPT-4o | Built with Streamlit & LangChain v0.3")