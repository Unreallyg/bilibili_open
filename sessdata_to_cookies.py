import json
from datetime import datetime
import time
import tkinter as tk
from tkinter import filedialog
import os

# 隱藏 tkinter 主視窗
root = tk.Tk()
root.withdraw()

# 取得目前 .py 腳本所在的目錄
script_dir = os.path.dirname(os.path.abspath(__file__))

# 讓使用者選擇 .json 檔案，預設開啟到腳本所在資料夾
print("請選擇你的 Bilibili cookies .json 檔案...")
json_path = filedialog.askopenfilename(
    title="選擇 Bilibili cookies JSON 檔案",
    initialdir=script_dir,
    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
)

if not json_path:
    print("未選擇檔案，程式結束。")
    input("按 Enter 結束...")
    exit()

print(f"已選擇檔案：{json_path}")

# 嘗試讀取 JSON，忽略 rawdata 相關問題
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除 rawdata 整個欄位（從 "rawdata": 開始到最後一個 } 前）
    # 這是最粗暴但有效的辦法，避免 rawdata 裡的控制字元或換行問題
    if '"rawdata":' in content:
        start_idx = content.find('"rawdata":')
        if start_idx != -1:
            # 找到 rawdata 開始，往前找前一個逗號或 { 來切斷
            comma_before = content.rfind(',', 0, start_idx)
            if comma_before != -1:
                content = content[:comma_before] + content[content.rfind('}', start_idx):]
            else:
                # 如果是第一個欄位，直接切到後面
                content = content[:start_idx] + content[content.find('}', start_idx):]
    
    # 再試一次解析
    data = json.loads(content)
    print("JSON 解析成功（已忽略 rawdata 欄位）")

except json.JSONDecodeError as e:
    print("JSON 解析失敗，即使忽略 rawdata 也無法讀取：")
    print(str(e))
    print("\n建議：")
    print("1. 用記事本開啟原 .json 檔")
    print("2. 刪除整個 \"rawdata\": ... 那一行（包含前面的逗號）")
    print("3. 存成 UTF-8 後再試一次")
    input("\n按 Enter 結束程式...")
    exit()

except Exception as e:
    print("讀取檔案時發生其他錯誤：", str(e))
    input("按 Enter 結束...")
    exit()

# 主要 cookies 字典（只用前面的欄位）
cookies = {
    'buvid3': data.get('buvid3'),
    'b_nut': data.get('b_nut'),
    'SESSDATA': data.get('SESSDATA'),
    'bili_jct': data.get('bili_jct'),
    'DedeUserID': data.get('DedeUserID'),
    'DedeUserID__ckMd5': data.get('DedeUserID__ckMd5'),
    'sid': data.get('sid'),
}

# expires 處理（大多數用這個時間）
expires_str = data.get('expires', '2025-10-26 13:05:35Z')
if expires_str.endswith('Z'):
    expires_str = expires_str[:-1].strip()

try:
    dt = datetime.strptime(expires_str, '%Y-%m-%d %H:%M:%S')
    expires_unix = int(time.mktime(dt.utctimetuple()))
except:
    expires_unix = 0
    print("警告：expires 格式無法解析，使用 0（不過期）")

# buvid3 和 b_nut 給較長有效期（2026-01-03）
long_expires = 1767424783

# 產生 Netscape 格式內容
output_lines = [
    "# Netscape HTTP Cookie File",
    "# Generated for yt-dlp from Bilibili JSON (rawdata 已忽略)",
    "# https://github.com/yt-dlp/yt-dlp",
    "",
]

domain = ".bilibili.com"
path = "/"
is_subdomain = "TRUE"
secure = "TRUE"

for name, value in cookies.items():
    if value is None or value == "":
        continue
    
    exp = long_expires if name in ['buvid3', 'b_nut'] else expires_unix
    
    line = f"{domain}\t{is_subdomain}\t{path}\t{secure}\t{exp}\t{name}\t{value}"
    output_lines.append(line)

# 輸出到 .py 同目錄
output_file = os.path.join(script_dir, "bilibili_cookies.txt")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"\n成功生成：{output_file}")
print("前幾行預覽：")
for line in output_lines[:10]:
    print(line)

print("\n轉換完成！你可以直接把這個 bili_cookies.txt 用在 yt-dlp / Open Video Downloader。")
input("按 Enter 關閉視窗...")
