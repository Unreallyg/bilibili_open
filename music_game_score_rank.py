import re

def generate_default_names():
    """生成從 AA 到 ZZ 的默認名稱列表"""
    return [chr(65 + i) + chr(65 + j) for i in range(26) for j in range(26)]

def parse_song_data(existing_songs, used_names, first_run=True):
    """解析歌曲數據，保留現有歌曲並支持新增與刪除"""
    songs = existing_songs[:]
    default_names = generate_default_names()
    default_name_index = len(songs)  # 從現有歌曲數量開始分配默認名稱
    if first_run:
        print("\n歌曲數據（格式：七位數或S+八位數[自定義名稱]，例：1337931EXIST 或 S13001011SE；七位數：前四位耗時（MSSS，例：1300表示1分30.0秒），後三位得分；八位數以S開頭，前四位耗時，後四位得分；D+名稱刪除歌曲，例：DAA）")
    print("現有歌曲：", ", ".join(f"{song[0]}: {song[3]}{song[0] if song[0] not in default_names else ''}" for song in songs) if songs else "無")
    
    while True:
        # 找到下一個未使用的默認名稱
        while default_name_index < len(default_names) and default_names[default_name_index] in used_names:
            default_name_index += 1
        if default_name_index >= len(default_names):
            print("默認名稱已用盡！請提供自定義名稱。")
            break
        
        default_name = default_names[default_name_index]
        try:
            song_input = input(f"歌曲{default_name}: ").strip()
            if song_input == "":
                break
            
            # 檢查是否為刪除操作
            if song_input.startswith('D'):
                song_name = song_input[1:].strip()
                if not song_name:
                    print("請提供要刪除的歌曲名稱！")
                    continue
                for i, (name, _, _, _) in enumerate(songs):
                    if name == song_name:
                        songs.pop(i)
                        used_names.remove(song_name)
                        print(f"已刪除歌曲 {song_name}")
                        break
                else:
                    print(f"歌曲 {song_name} 不存在！")
                continue
            
            # 使用正則表達式提取七位數或八位數及自定義名稱
            match = re.match(r"^(S?\d{7,8})(\S*)$", song_input)
            if not match:
                print("格式錯誤，請輸入七位數字或S+八位數字（可選後跟自定義名稱）！")
                continue
            
            number_part = match.group(1)
            custom_name = match.group(2) if match.group(2) else None
            is_eight_digit = number_part.startswith('S')
            number = number_part[1:] if is_eight_digit else number_part
            
            # 驗證數字長度
            if (is_eight_digit and len(number) != 8) or (not is_eight_digit and len(number) != 7):
                print("格式錯誤，七位數或S+八位數！")
                continue
            
            # 解析耗時（前四位，單位：秒）
            time_str = number[:4]
            try:
                minutes = int(time_str[0])  # 第一位表示分鐘
                seconds = int(time_str[1:]) / 10  # 第二至第四位表示秒，精確到 0.1秒
                time = minutes * 60 + seconds  # 總秒數
                score = int(number[4:])   # 分數（七位數後三位，八位數後四位）
            except ValueError:
                print("耗時或得分格式錯誤，請檢查！")
                continue
            
            # 確定歌曲名稱
            song_name = custom_name if custom_name else default_name
            if song_name in used_names:
                print(f"名稱 {song_name} 已存在，請使用其他名稱！")
                continue
            
            songs.append((song_name, time, score, number_part))
            used_names.add(song_name)
            default_name_index += 1
        
        except Exception as e:
            print(f"輸入無效，請重新輸入（錯誤：{e}）！")
            continue
    
    return songs, used_names

def get_event_params():
    """獲取活動參數"""
    while True:
        try:
            days = int(input("活動持續天數："))
            if days <= 0:
                print("天數必須大於 0！")
                continue
            min_time = float(input("每天平均打歌最短時間（小時）："))
            max_time = float(input("每天平均打歌最長時間（小時）："))
            if min_time > max_time:
                print("最短時間不能大於最長時間！")
                continue
            step = float(input("計算步長（小時）："))
            if step <= 0:
                print("步長必須大於 0！")
                continue
            reload_time = float(input("每次重新加載時間（秒）："))
            if reload_time < 0:
                print("重新加載時間不能小於 0！")
                continue
            return days, min_time, max_time, step, reload_time
        except ValueError:
            print("請輸入有效數字！")
            continue

def calculate_rankings(songs, days, min_time, max_time, step, reload_time):
    """計算每個時間節點的總得分排行"""
    rankings = []
    current_time = min_time
    while current_time <= max_time:
        total_time = current_time * 3600 * days  # 總時間（秒）
        song_scores = []
        
        # 計算每首歌的總得分
        for song_name, time, score, _ in songs:
            cycle_time = time + reload_time  # 每次完整週期（打歌+加載）
            plays = total_time // cycle_time  # 整數次數
            # 檢查最後一次是否完成一半
            remaining = total_time % cycle_time
            if remaining < time / 2:
                plays -= 1
            total_score = plays * score
            song_scores.append((song_name, total_score))
        
        # 按總得分降序排序
        song_scores.sort(key=lambda x: x[1], reverse=True)
        
        # 計算百分比差異
        ranking_parts = []
        for i, (song_name, score) in enumerate(song_scores):
            if i < len(song_scores) - 1 and song_scores[i+1][1] > 0:
                next_score = song_scores[i+1][1]
                percentage = (1 - next_score / score) * 100
                ranking_parts.append(f"{song_name}({percentage:.1f}%)")
            else:
                ranking_parts.append(song_name)
        ranking = " > ".join(ranking_parts)
        rankings.append((current_time, ranking))
        
        current_time += step
    
    return rankings

def print_rankings(rankings):
    """打印排行結果"""
    print("\n各時間節點的總得分排行：")
    print("-" * 40)
    for time, ranking in rankings:
        # 時間 < 10 小時時，冒號後加空格以對齊
        space = " " if time < 10 else ""
        print(f"每天 {time:.1f} 小時:{space} {ranking}")
        print()  # 每個時間節點後加空行
    print("-" * 40)

def main():
    songs = []  # 儲存歌曲數據
    used_names = set()  # 記錄已使用的名稱
    first_run = True
    while True:
        songs, used_names = parse_song_data(songs, used_names, first_run)
        first_run = False
        if not songs:
            print("未輸入任何歌曲數據，重新開始！")
            continue
        days, min_time, max_time, step, reload_time = get_event_params()
        rankings = calculate_rankings(songs, days, min_time, max_time, step, reload_time)
        print_rankings(rankings)

if __name__ == "__main__":
    main()
