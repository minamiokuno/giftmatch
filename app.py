# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# ユーザーインターフェイスの構築
st.title("GiftMatch")
st.write("あなたの思いを形に。贈り先のパーソナリティに合った最適なギフトを提案します。")
st.image("present_01.webp")
st.title(" ")
st.write("プレゼントを贈りたいお相手のことを教えてください。")

# プルダウンメニューを表示（デフォルトは"選択してください"）
st.session_state["receiver_gender"] = st.selectbox("贈り先の方の性別を選択してください：", ["選択してください", "男性", "女性"], index=0)
st.session_state["receiver_age_group"] = st.selectbox("贈り先の方の年齢を選択してください：", ["選択してください", "10代", "20代", "30代", "40代", "50代", "60代以上"], index=0)
st.session_state["receiver_hobby_group"] = st.selectbox("贈り先の方の趣味を選択してください：", ["選択してください", "国内観光旅行", "海外旅行", "外食", "読書", "ドライブ", "映画", "音楽鑑賞", "ウィンドウショッピング", "温泉・サウナ", "カラオケ", "漫画・アニメ", "園芸", "ギャンブル", "ライブ・コンサート", "筋トレ・ジム", "マラソン・ジョギング", "バーベキュー", "遊園地", "ピクニック", "ペット", "ゲーム", "カメラ・写真", "スポーツ・観戦", "料理", "遊園地", "バー・飲み"], index=0)
st.session_state["receiver_brand"] = st.text_input("贈り先の方がすでに持っているブランドや商品を入力してください：", "")
st.session_state["receiver_object_group"] = st.selectbox("プレゼントの目的を選択してください：", ["選択してください", "誕生日", "記念日", "クリスマス", "バレンタインデー", "ホワイトデー", "結婚記念日", "母の日", "父の日", "敬老の日", "お中元", "お歳暮", "出産祝い", "入学祝い", "卒業祝い", "入社祝い", "退職祝い", "新築祝い", "快気祝い", "お見舞い", "謝礼", "お礼", "挨拶", "その他"], index=0)
st.session_state["receiver_money_group"] = st.selectbox("予算を選択してください：", ["選択してください", "1,000円以下", "1,000円〜3,000円", "3,000円〜5,000円", "5,000円~1万円", "1万円〜2万円", "2万円~3万円", "3万円~5万円", "5万円〜7万円", "7万円~10万円", "10万円~15万円", "15万円~20万円", "20万円以上"], index=0)
st.session_state["user_input"] = st.text_area("特記事項があればご記入ください:", "")

def communicate():
    # プルダウンメニューから選択された情報を取得
    receiver_gender = st.session_state["receiver_gender"]
    receiver_age_group = st.session_state["receiver_age_group"]
    receiver_hobby_group = st.session_state["receiver_hobby_group"]
    receiver_brand = st.session_state["receiver_brand"]
    receiver_object_group = st.session_state["receiver_object_group"]
    receiver_money_group = st.session_state["receiver_money_group"]

    user_input = ""
    if receiver_gender != "選択してください":
        user_input += "贈り先の性別：" + receiver_gender + "\n"
    if receiver_age_group != "選択してください":
        user_input += "贈り先の年齢：" + receiver_age_group + "\n"
    if receiver_hobby_group != "選択してください":
        user_input += "贈り先の趣味：" + receiver_hobby_group + "\n"
    if receiver_brand != "":
        user_input += "贈り先の持っているブランドや商品：" + receiver_brand + "\n"
    if receiver_money_group != "選択してください":
        user_input += "プレゼントの予算：" + receiver_money_group + "\n"
    if receiver_object_group != "選択してください":
        user_input += "プレゼントの目的：" + receiver_object_group + "\n"
    if st.session_state.get("user_input", ""):
        user_input += "特記事項：" + st.session_state.get("user_input", "") + "\n"

    # ユーザーが選択したオプションとテキスト入力を用いてGPT-3へのプロンプトを作成
    system_prompt = f"""
    あなたは相手に喜んでもらえるプレゼントを提案するプロです。以下の情報に基づいて、適切なプレゼントを提案してください。
    {user_input}
    これらの情報を元に、適切なプレゼントを5~10個提案してください。
    具体的なブランド名と商品名を提案してください。
    それぞれがなぜ適しているのか説明も添えてください。
    また、贈り先が既に持っているブランドや商品そのものは避け、その趣味や嗜好を反映した新たなアイテムを提案してください。
    
    * GiftMatchはとても明るく前向きな言葉を使います。
    * びっくりマークが多いです
    GiftMatchのセリフ
    * プレゼントを提案した最後に「お相手に喜んでいただけますように！」という言葉をつけます
    """

    messages = st.session_state["messages"]
    user_message = {"role": "user", "content": user_input}  
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去
    return bot_message['content']

# Here we add a button
# ボタンがクリックされたときにcommunicateを呼び出す
if st.button("送信する"):
    # "messages"キーを初期化
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    bot_response = communicate()
    st.write(bot_response)
