import streamlit as st
import pandas as pd
import time
import requests
from PIL import Image
import base64
from aip import AipSpeech
import os;
from pydub import AudioSegment
import io;
from io import BytesIO
from collections import Counter
import re

#页面设置
st.set_page_config(
    page_title="SourceHunter",
    page_icon="💬",
    layout="centered",
)

# 百度图片搜索API的URL和密钥
BAIDU_API_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
BAIDU_API_KEY = "24.7f90849de5d87722f8402d34e9272c90.2592000.1731590882.282335-115880616"

#定义对图片编码base64格式的函数
def image_to_base64(file):
    return base64.b64encode(file.read()).decode('utf-8')

# 调用百度图片搜索API的函数
def baidu_image_search(file):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        'access_token': BAIDU_API_KEY,
        'image': file,
    }
    response = requests.post(BAIDU_API_URL, headers=headers, data=payload)
    return response.json()
# 百度智能云的APP_ID, API_KEY, SECRET_KEY
APP_ID = '115908451'
API_KEY = 'R6rdmN5AvFyIEEswnRhKzd45'
SECRET_KEY = 'QtbMkUjcRwoVKdhw5CxpXUnBmdxL6pv2'

# 初始化AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取语音文件
def get_file_content(file):
    # 直接返回上传的文件对象内容
    return file.read()

# 百度智能云API密钥
API_KEY = 'yrLwr2dEwmlh1ryZPdDp8WnH'
SECRET_KEY = 'jB7QbEyNmleex72b4oJhIQlb06fJn62N'

# 获取访问令牌
def get_access_token():
    url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SECRET_KEY}'
    response = requests.post(url)
    return response.json().get('access_token')

# 调用文字识别API
def ocr_image(image_path):
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    access_token = get_access_token()
    url = f'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}'
    payload = {'image': image_data}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.post(url, data=payload, headers=headers)
    return response.json()

# 转换音频格式
def convert_audio_to_pcm(file, format):
    audio = AudioSegment.from_file(file, format=format)
    pcm_file = "converted_audio.wav"
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)  # 设置采样率为 16000
    audio.export(pcm_file, format="wav")  # 导出为 PCM WAV 格式
    with open(pcm_file, 'rb') as f:
        pcm_content = f.read()
    os.remove(pcm_file)
    return pcm_content

# 调用百度智能云语音识别API
def recognize_speech(file_content):
    if not file_content:
        return {"error": "文件读取失败"}

    try:
        # 检查file_content的类型
        if isinstance(file_content, bytes):
            print("文件内容类型正确，准备调用API")
            result = client.asr(file_content, 'wav', 16000, {
    'dev_pid': 1537,  # 普通话
    'cuid': '123456',  # 用户设备唯一标识
    'token': 'your_access_token',  # 可选，若需要 token 验证
})
            print("API 返回结果:", result)  # 打印返回结果
            return result
        else:
            return {"error": "文件内容应为字节类型"}
    except Exception as e:
        st.error(f"识别过程中发生错误：{e}")
        return {"error": str(e)}
    
# 示例：识别语音文件并输出结果
file_path = 'path_to_your_audio_file.wav'
result = recognize_speech(file_path)
print(result)

#页面背景及侧边栏背景设置
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%);
    }

    .st-emotion-cache-dvne4q {
        background-image: linear-gradient(120deg, #fccb90 0%, #d57eeb 100%);
    }

    .eczjsme4 {
        background-image: linear-gradient(120deg, #fccb90 0%, #d57eeb 100%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

#tabs初始化
home,pic_search,audio_search,word_search,mine = st.tabs(["🏠首页","🔍图片搜索","🎵音频搜索","📄文字搜索","🛋️我的"])

#tabs及标题样式
with home:
    st.markdown(
        """
    <style>
    .center-container {
        position: relative;
        height: 500px;
        width: 500px;
        margin: 0 auto; 
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeIn 1s ease-in-out; /* 添加淡入动画 */
    }

    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }

.box {
    position: relative;
    width: 320px;
    height: 180px;
    background: linear-gradient(135deg, #d9a7c7, #fffcdc);
    border-radius: 15px;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 4px solid;
    border-image: linear-gradient(135deg, #a6c0fe, #f68084) 1;
    box-shadow: inset 0 4px 6px rgba(0, 0, 0, 0.1), 0 8px 15px rgba(0, 0, 0, 0.2); /* 外加内阴影 */
    }

    .title {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 50px;
        color: #5c307d;
        text-align: center;
    }

.button {
    background: linear-gradient(120deg, #a6c0fe 0%, #f68084 100%); /* 浅蓝到粉红的渐变 */
    color: white;
    padding: 15px 20px;
    text-align: center;
    border-radius: 10px;
    font-size: 16px;
    width: 150px;
    cursor: pointer;
    position: absolute;
    transition: background 0.3s ease;
}


.button:hover {
    box-shadow: 0 0 15px rgba(246, 141, 195, 0.7), 0 0 30px rgba(246, 141, 195, 0.5);
    transform: scale(1.1) rotate(5deg); /* 放大并轻微旋转 */
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3); /* 提升阴影效果 */
    background: linear-gradient(120deg, #f9a8d4 0%, #f68084 100%); /* 悬停时使用粉紫到粉红的渐变 */
}

    /* 四个功能按钮的位置，左上、左下、右上、右下 */
    .button-top-left {
        top: 70px;
        left: 10px;
    }

    .button-bottom-left {
        bottom: 70px;
        left: 10px;
    }

    .button-top-right {
        top: 70px;
        right: 10px;
    }

    .button-bottom-right {
        bottom: 70px;
        right: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
    )

# 在页面中显示标题和按钮
    st.markdown(
    """
    <div class="center-container">
        <div class="box">
            <div class="title">SourceHunter</div>
        </div>
        <button class="button button-top-left" onclick="window.location.href='🔍图片搜索'">🔍图片搜索</button>
        <button class="button button-top-right" onclick="window.location.href='🎵音频搜索'">🎵音频搜索</button>
        <button class="button button-bottom-left" onclick="window.location.href='📃文字搜索'">📄文字搜索</button>
        <button class="button button-bottom-right" onclick="window.location.href='🛋️我的'">🛋️我的</button>
    </div>
    """, 
    unsafe_allow_html=True
    )

#侧边栏初始化
st.sidebar.title("SourceHunter")
st.sidebar.header("Welcome!欢迎使用")
st.sidebar.markdown("**以下是相关说明**")
st.sidebar.markdown("**创意背景:**")
st.sidebar.markdown("在数字时代，音频和图像的使用日益广泛，尤其是在社交媒体、在线学习和内容创作领域。为了满足用户对多媒体内容的高效管理和搜索需求，我们开发了这款基于Streamlit的应用。该应用旨在通过友好的界面和高效的搜索功能，为用户提供一个便捷的多媒体管理平台，使他们能够轻松查找、使用和管理音频与图像资源。")
st.sidebar.markdown("**用户群体:**")
st.sidebar.markdown("1.内容创作者:如博主、视频制作人和社交媒体管理者，他们需要快速找到并使用高质量的音频和图像资源来提升内容的吸引力。  \n2.学生和教育工作者:在学习和教学过程中，音频和图像可以帮助更好地理解和传达知识。因此，他们需要一个易于访问和搜索的工具来整合这些资源。  \n3.设计师和开发者：需要管理和搜索大量设计素材和音频样本，以便在项目中灵活使用。")
st.sidebar.markdown("**功能特征:**")
st.sidebar.markdown("1.多媒体搜索功能:用户可以通过关键字快速搜索音频和图像，提高了内容查找的效率。该功能支持历史记录追踪，方便用户查看和重用之前的搜索结果。  \n2.用户友好的界面：应用界面设计简洁直观，用户可以轻松导航和使用不同功能，提升了用户体验。  \n3.关键词跟踪：为了确保搜索的有效性，应用提供关键词跟踪功能，用户能够查看和管理搜索历史，提高了后续使用的便捷性。  \n4.一致的展示风格：音频和图像搜索结果在视觉呈现上保持一致，为用户提供了良好的审美体验，增强了整体使用的流畅感。")

#图片搜索tab
with pic_search:
    #图片搜索文案动画
    st.markdown(
        """
        <div class='tab-content'>
        <h2>
        Picture Search图片检索🔍\n
        请在下方上传**你的图片**(支持png,jpg,gif格式)，以获得其详细内容
        </h2>
        </div>
        """,
        unsafe_allow_html=True
        )
    uploaded_file = st.file_uploader("请上传你的图片", type=['png','jpg','gif'], accept_multiple_files=False, key=None, help=None, on_change=None, args=None, kwargs=None)
    if uploaded_file is not None:
    # 将上传的文件转换为 Base64 编码
        file_encoded = image_to_base64(uploaded_file)

    #提交按钮设置
    if st.button("Submit提交", key='button_picsearch'):
        st.markdown("请稍后……")
        pic_result = baidu_image_search(file_encoded)
        time.sleep(2)
        json_response = pic_result  # 显示API返回的JSON结果

        #设置搜索返回内容的UI
        st.title("识别结果展示")

        if "result" in json_response and json_response["result"]:
            # 按照分数排序，选择最高分的结果
            top_result = max(json_response["result"], key=lambda x: x['score'])

        # 显示 log_id 和结果数量
        st.markdown(f"**Log ID:** {json_response['log_id']}")
        st.markdown(f"**结果数量:** {json_response['result_num']}")

        # 使用 Streamlit 的 columns 来制作更加美观的布局
        for item in json_response["result"]:
            col1, col2, col3 = st.columns([2, 2, 1])
        
            # 展示关键字和根类
            with col1:
                st.markdown(f"**关键词:** {item['keyword']}")
            
            with col2:
                st.markdown(f"**根类别:** {item['root']}")
            
            with col3:
                st.markdown(f"**分数:** {item['score']:.2f}")
        
            # 添加分割线
            st.markdown("---")

        # 结尾的一个总结
        st.success("以上为识别出的相关信息。")

#音频搜索tab
with audio_search:
    st.header("Audio Search音频识别🎵")
    st.markdown("**短句语音转文字**，请在下方上传你的音频文件 (支持wav,m4a,mp3格式)，以获取识别结果。")

    # 上传音频文件
    audio_file = st.file_uploader("请上传你的音频文件", type=['wav','mp3','m4a'], accept_multiple_files=False)


if audio_file is not None:
    file_extension = audio_file.name.split('.')[-1].lower()
    
    # 调用相应格式的处理函数
    if file_extension in ['wav', 'mp3', 'm4a']:
        file_content = convert_audio_to_pcm(audio_file, file_extension)
        
        # 调用语音识别函数
        result = recognize_speech(file_content)
        
        # 展示识别结果
        if 'result' in result:
            st.success("识别结果：")

    # 将每一句识别结果用卡片样式展示
            st.markdown("""
     <style>
    .result-card {
        background-color: rgba(255, 255, 255, 0.3);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
        color: #3c3c3c;
        font-family: 'Arial', sans-serif;
        font-size: 1.1em;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .result-card:hover {
        background-color: rgba(255, 255, 255, 0.5);
        transition: background 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # 遍历识别结果并用美化样式输出
            for sentence in result['result']:
                st.markdown(f'<div class="result-card">{sentence}</div>', unsafe_allow_html=True)
        else:
            st.error("识别失败，请重试。")
    else:
        st.error(f"不支持的音频格式: {file_extension}")

with word_search:
    st.header("Picture to Text图片转文字📷")
    st.markdown("**图片转文字**，请在下方上传你的图片文件 (支持png,jpg,gif格式)，以获取识别结果。")

    # 上传图片文件
    image_file = st.file_uploader("请上传你的图片文件", type=['png', 'jpg', 'gif'], accept_multiple_files=False)

if image_file is not None:
    # 将图片文件保存并传递到 OCR 识别函数
    with open("temp_image.png", "wb") as f:
        f.write(image_file.getbuffer())
    
    # 调用 OCR 识别函数
    result = ocr_image("temp_image.png")
    
    if 'words_result' in result and result['words_result']:
        st.success("识别结果：")

        # 将所有识别出的文字拼接成一段文字
        full_text = "\n".join([word_info["words"] for word_info in result['words_result']])

        # 使用 card 样式展示整段文字
        st.markdown("""
        <style>
        .doc-card {
            background-color: rgba(255, 255, 255, 0.3);  /* 浅白色背景带透明度 */
            padding: 20px;
            border-radius: 12px;
            box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.1);
            color: #3c3c3c;  /* 深灰色字体 */
            font-family: 'Arial', sans-serif;
            font-size: 1.1em;
            backdrop-filter: blur(10px);  /* 背景模糊效果 */
            border: 1px solid rgba(255, 255, 255, 0.2); /* 边框半透明 */
            line-height: 1.6; /* 增加行间距 */
            white-space: pre-wrap;  /* 保留换行 */
        }
        </style>
        """, unsafe_allow_html=True)

        # 使用美化后的卡片样式输出整段文字
        st.markdown(f'<div class="doc-card">{full_text}</div>', unsafe_allow_html=True)
    else:
        st.error("识别失败，请重试。")

#我的tab
with mine:
    st.markdown("""
<style>
    .tag {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2); /* 半透明背景 */
        color: #3c3c3c; /* 深灰色字体 */
        padding: 8px 12px;
        margin: 5px;
        border-radius: 16px;
        font-size: 0.9em;
        font-family: 'Arial', sans-serif;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.3); /* 半透明边框 */
    }
    .tag:hover {
        background-color: rgba(255, 255, 255, 0.4); /* 悬停时背景色稍微加深 */
    }
</style>
""", unsafe_allow_html=True)
    col1,col2 = st.columns([4,5])
    col1.image("data/SourceHunter.png", width=200)
    col2.header("**名称**：SourceHunter")
    sex = col2.selectbox(
        label = '请输入您的性别',
        options = ('男', '女', '保密'),
        index = 2,
        format_func = str,
        help = '如果您不想透露，可以选择保密'
        )
    if sex == '男':
        col2.markdown("**性别**：男")
    elif sex == '女':
        col2.markdown("**性别**：女")
    else:
        col2.markdown("**性别**：未知")
    age = col2.slider(label='请输入您的年龄', 
                    min_value=0, 
                    max_value=100, 
                    value=0, 
                    step=1, 
                    help="请输入您的年龄"
                    )