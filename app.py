import streamlit as st
from openai import OpenAI

# ========== 在這裡貼上你的 API Key ==========
API_KEY = "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"
MODEL_NAME = "openrouter/free"

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="嶺南大學新生導航助手", page_icon="🎓")
st.title("嶺南大學新生校園服務導航助手")
st.caption("可以問我關於學生證、住宿、圖書館、醫療、繳費等問題")

KNOWLEDGE = """你是嶺南大學的新生校園服務導航助手。

【最重要規則】
- 必須優先且主要（約 90%）使用下面「新生指南」的內容回答。
- 只有指南完全沒提到的細節，才可以稍微補充，並標明「以下是補充資訊」。
- 絕對不要編造指南裡沒有的電話、網址、費用或流程。
- 如果指南沒有相關資訊，就說：「根據新生指南，目前沒有詳細說明，建議到嶺南大學官網 https://www.ln.edu.hk 或聯絡相關部門確認。」

【新生指南完整內容】

一、宿舍住宿與報修指南
嶺大共有 10 座學生宿舍。宿位申請、宿務管理與舍堂生活由學生事務處（OSA）負責；宿舍設施維修與校園工程由校園發展及管理處（OCDM）負責。
4年2宿政策：全日制本地本科生在 4 年學制內獲保障最少 2 年住宿期；非本地生獲優先保障全期住宿。
網上申請：Year 1 新生收到錄取通知後，須於指定期限內登入 myLingnan Portal 完成宿位申請。
房型主要為雙人房（Twin Room），少量為三人房。舍堂與室友（同性別）由系統隨機抽籤分配，無法自選樓棟。
住宿期限：每期宿位有效期為一個完整學年（約 9 個月），涵蓋上、下學期。暑期住宿需另行提交申請。
費用：學期住宿費按學年分兩期收取，本科生每學期約 HK$5,000–$7,500 不等（依房型而定）。登入 myLingnan Portal 下載 eFees Note 電子繳款單，透過網上銀行、ATM 或 PPS 繳付。
基本水電與 Wi-Fi：房內基礎照明、插座供電、浴室熱水及校園 Wi-Fi/LAN 網絡全免，已包含於學期住宿費內。
房間冷氣費：採用「用者自付」原則，房間設有冷氣讀卡計費器，室友共用。使用八達通於房內冷氣計費器直接感應儲值。
公共洗衣與乾衣：舍堂公共洗衣房，洗衣機每次約 HK$6，乾衣機約 HK$1 / 7 分鐘，直接刷八達通卡付費。
報修流程：
1. 地下保安櫃檯現場登記（最快）：房內設施故障，直接親臨所屬宿舍地下保安櫃檯填寫紙本報修單。
2. 電郵 ocdmcs@LN.edu.hk 或致電專線 (852) 2616 7134 通報。
3. 維修師傅接單後將於辦公時間內進入房間排查維修。如超過 3 天未獲處理，可致電專線追蹤。
費用承擔：自然損耗免費維修；因人為破壞或遺失鑰匙/門卡者需照價賠償。
宿舍生活守則：
- 訪客時間：每日 08:00 至 23:00。所有訪客必須於地下保安櫃檯登記。23:00 後嚴禁非該舍堂住客逗留。
- 全域禁煙與禁酒：宿舍範圍內（含房間、走廊及露台）嚴禁吸煙（含電子煙）、無牌飲酒及賭博。
- 高功率電器限制：房內嚴禁使用電磁爐、電飯煲、電暖爐等高功率加熱電器，違者沒收。此類電器僅限於公共茶水間使用。
緊急聯絡：
- OSA 宿務：電話 (852) 2616 7368，電郵 osa-hostel@ln.edu.hk。
- OCDM 設施維修：電話 (852) 2616 7134，電郵 ocdmcs@LN.edu.hk。
- 24小時校園緊急求助熱線：(852) 2616 8000。

二、醫療與緊急求助指南
緊急求助提示：若遇生命危險或重大突發事故，請優先撥打嶺南大學 24小時校園緊急求助熱線 (852) 2616 8000，或直撥香港緊急救援電話 999。
學生西醫醫療計劃：校方指定特約西醫診所（距校園最近為富泰商場地下 3 號舖「盈健醫務中心 PHC Medical Centre」）。出示學生證及香港身份證，每次診症僅需繳付約 HK$20。
嶺南大學中醫診所：位於校園訪客宿舍 G01 室（Visitors' Quarters VQG01），近南門。提供中醫師內科診症、針灸、骨傷正骨及中藥配藥服務。電話 (852) 2616 7828，可透過網上預約系統提早預約。
學生牙科保健計劃：指定合作牙科診所（涵蓋屯門及全港多區），提供每年一次洗牙、基本檢查及優惠價牙科治療。需提前向 OSA 或診所預約。
離校最近之公立醫院：屯門醫院。急症室地址：新界屯門青松觀路 23 號。查詢電話 (852) 2468 5111（24 小時）。持香港身份證學生於急症室求診每次費用為 HK$180。
校園保安：
- 24小時緊急熱線：(852) 2616 8000。
- 保安控制中心：(852) 2616 8705。
- 設施緊急維修：(852) 2616 7134 / 2616 7139。
心理輔導與情緒支援：
- 校園輔導中心：劉李麗雲樓 3 樓 LYH318 室。
- 預約輔導專線：(852) 2616 7024，電郵 counsel@LN.edu.hk。辦公時間：週一至五 09:00–12:30, 13:30–17:21。
- 嶺大宿生 24 小時心理輔導熱線：(852) 2616 8866（由基督教家庭服務中心支援）。

三、學生證（LU Card）服務指南
嶺南大學學生證是校內身份識別、門禁進出、宿舍管理及圖書館借閱的唯一官方憑證。
Year 1 新生申請：接獲錄取後，登入 myLingnan Portal 大學網上報到系統上載符合規格的電子相片。完成網上報到手續後，於開學前指定日期憑香港身份證/護照親臨教務處領取。
首次申請費用：全日制及兼讀制新生獲發的首張實體學生證完全免費。
相片規格要求：
- 檔案格式與大小：必須為 JPEG 或 JPG 格式，檔案大小不得超過 5MB。
- 解析度與尺寸：像素尺寸最少為 600 像素（寬）× 750 像素（高）（比例約 4:5）。
- 人像：必須為近 6 個月內拍攝的正頭像，面部清晰，由下巴至頭頂高度須佔整張相片高度的 60% 至 70%。不可佩戴帽子、深色眼鏡或遮擋面部的飾物。
- 背景必須為純白色。
遺失、損壞與補辦：
- 補辦手續費：每張新卡費用為港幣 HK$100。舊卡因損壞補辦者須繳回舊卡。
- 申請方式：1. 網上申請（登入 myLingnan Portal 遞交申請並繳費）；2. 現場辦理（親臨教務處櫃檯填寫表格，可用八達通繳費）。
- 所需材料：香港身份證或護照正本、繳費證明、如原卡損壞需交回舊卡。
- 製作時間：一般需時 5 個工作天。
教務處聯絡資訊：
- 地址：香港新界屯門青山公路 8 號 嶺南大學王黃鳳鳴行政大樓地下 ADG08 室。
- 辦公時間：星期一至五 上午 09:00 – 下午 12:30，下午 01:30 – 下午 05:36。星期六、日及公眾假期休息。
- 電話：(852) 2616 8750，電郵：UGadm@LN.edu.hk / Registry@LN.edu.hk。
- 官網：https://www.ln.edu.hk/reg

四、圖書館基礎服務指南
嶺南大學圖書館（Fong Sum Wood Library / 鄺森活圖書館）。
開放時間：
- 圖書館主館：星期一至五 08:30 – 22:00；星期六 09:00 – 17:00；星期日 13:00 – 17:00。
- 24小時研習區：全天 24 小時開放（位於一樓，憑學生證刷卡進入）。
- 諮詢服務台：星期一至五 09:00 – 19:00；星期六 09:00 – 17:00；星期日不開放。
借閱規則：
- 學士學位學生最多借閱 100 冊，一般圖書借期最長 90 天。
- 還書：可在開館時間於服務櫃檯歸還，或於閉館期間使用圖書館正門外的 24小時還書箱。
- 逾期罰款：一般圖書每本每日港幣 HK$1.00；指定參考書（2小時借期）每小時港幣 HK$5.00。
館內設施：小組研討室可透過空間預約系統預訂；提供公用電腦、八達通付費影印及無線列印。
HKALL：若嶺大圖書館無所需書籍，可透過 1-Search 系統使用 HKALL 免費借閱香港其餘 7 所大學圖書館的藏書。
聯絡方式：
- 官網：https://www.library.ln.edu.hk/
- 電話：(852) 2616 8586
- WhatsApp：(852) 5981 7688
- 電郵：ref@ln.edu.hk

五、IT 帳號與網絡連接指南
嶺大實行單一帳號機制。LU Account 格式為 username，學生個人電郵為 username@ln.hk。
可存取：myLingnan Portal、Moodle、Microsoft 365、圖書館與公共電腦等。
帳號啟用：教務處會在入學前發送含學號及初始預設密碼的信件。首次登入 myLingnan Portal 完成密碼修改。
密碼要求：長度最少 8 至 12 位，需混合大寫字母、小寫字母、數字及特殊符號。
忘記密碼：可進入 selfservice.ln.edu.hk 自助重置。若帳號遭鎖定，可攜帶身份證件至 ITSC 服務台求助。
雙重認證（Duo Mobile）：
1. 在手機下載 Duo Mobile App。
2. 到 2fa.ln.edu.hk 登入並點擊 Enroll 2FA，掃描 QR Code 完成綁定。
3. 日常登入時點擊 Send me a Push，在手機上 Approve。
校園 Wi-Fi：
- LU / LU-Advanced：用嶺大帳號 username 登入。
- eduroam：用完整電郵 username@ln.hk 登入。
VPN：使用 F5 Access / BIG-IP。伺服器地址必須輸入 https://studentvpn2.ln.edu.hk。
ITSC 服務台：
- 地址：嶺南大學主樓 2 樓 MB203 室。
- 開放時間：星期一至五 08:30 – 17:20。
- 電話：(852) 2616 7995
- 電郵：itsc@ln.edu.hk
- 官網：www.ln.edu.hk/itsc/services

官方網站匯總：
- 嶺大官網：https://www.ln.edu.hk
- 學生事務處（OSA）：https://www.ln.edu.hk/osa
- 教務處（Registry）：https://www.ln.edu.hk/reg
- 圖書館：https://www.library.ln.edu.hk
- ITSC：https://www.ln.edu.hk/itsc
- 中醫診所：www.ln.edu.hk/cmc
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": KNOWLEDGE}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("請輸入你的問題...", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=st.session_state.messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
