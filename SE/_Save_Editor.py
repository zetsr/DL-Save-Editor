import sys  
import os
import shutil
import binascii

def bytes_to_hex(byte_data):
    """
    将字节数据转换为连续的HEX字符串
    例如：b'\x00\x01\x02\x03' -> '00010203'
    """
    return binascii.hexlify(byte_data).decode('utf-8').upper()

def hex_to_bytes(hex_str):
    """
    将连续的HEX字符串转换为字节数据
    例如：'00010203' -> b'\x00\x01\x02\x03'
    """
    return binascii.unhexlify(hex_str)

def format_hex_with_spaces(hex_str):
    """
    将连续的HEX字符串格式化为每个字节之间有一个空格的形式
    例如：'00010203' -> '00 01 02 03'
    """
    return ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))

def get_file_path():
    """
    获取文件路径，无论是通过拖拽还是用户输入
    """
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path) and file_path.lower().endswith('.sav'):
            return file_path
        else:
            print("拖拽的文件无效，请确保是一个.sav文件。")
            input("按回车键退出...")
            sys.exit(1)
    # 如果没有拖拽文件，提示用户输入文件路径
    while True:
        file_path = input("请输入.sav文件的完整路径（或将文件拖拽到此窗口后按回车）：").strip('"')
        if os.path.isfile(file_path) and file_path.lower().endswith('.sav'):
            return file_path
        else:
            print("文件无效，请确保路径正确且文件是.sav格式。")

def copy_and_rename(file_path):
    """
    复制文件并重新命名为原始名称，将新文件复制到脚本所在目录下的 output 文件夹中。
    新增：如果 output 目录不存在则创建。
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(directory, "output")
    # 如果 output 目录不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    original_name = os.path.basename(file_path)
    new_name = f"{original_name}"
    new_path = os.path.join(output_dir, new_name)
    try:
        shutil.copyfile(file_path, new_path)
        print(f"文件已复制并重命名为 {new_name}")
    except Exception as e:
        print(f"错误：无法复制并重命名文件。详细信息：{e}")
        input("按回车键退出...")
        sys.exit(1)
    return new_path

def find_string(hex_data, search_str):
    """
    在HEX数据中查找指定字符串的起始索引
    返回找到的起始索引，如果未找到则返回-1
    """
    search_hex = bytes_to_hex(search_str.encode('utf-8'))
    index = hex_data.find(search_hex)
    return index

def read_bytes_after(hex_data, start_index, offset, length):
    """
    从指定起始索引后偏移一定量读取指定长度的字节
    start_index: 起始索引（HEX字符串中的位置）
    offset: 偏移的字节数
    length: 读取的字节数
    返回读取的连续HEX字符串
    """
    start = start_index + offset * 2  # 每个字节用两个HEX字符表示
    end = start + length * 2
    return hex_data[start:end]

def validate_numeric_hex(hex_str, expected_length=None, prefix=None):
    """
    验证HEX字符串是否代表纯数字，并可选验证长度和前缀
    """
    try:
        bytes_data = hex_to_bytes(hex_str)
        digits = bytes_data.decode('utf-8')
        if expected_length and len(digits) != expected_length:
            return False
        if prefix and not digits.startswith(prefix):
            return False
        return digits.isdigit()
    except:
        return False

def output_saved_gender(role, saved_gender):
    """
    输出 SavedGender 信息，并在后面提示 0=Female, 1=Male
    """
    gender_str = "Female" if saved_gender == 0 else "Male"
    print(f"角色{role}的性别: {saved_gender} *{gender_str}*")

def output_saved_skin_index(role, saved_skin_index):
    """
    输出 SavedSkinIndex 信息，并根据角色不同输出对应的对照表
    """
    skin_maps = {
        "FS": {
            '00': "Random Skin",
            '01': "Melanistic KS",
            '02': "Leucistic KS",
            '03': "Leumelan KS",
            '04': "Crimson PT",
            '05': "Sandslayer",
            '06': "Snowslayer",
            '07': "Melanistic KS19",
            '08': "Leucistic KS19",
            '09': "Leumelan KS19",
            '0A': "Iconic",
            '0B': "Crimson LT",
            '0C': "Overo",
            '0D': "Lava Flow",
            '0E': "Swamp Geyser",
            '0F': "Burning Bright",
            '10': "Lava Ash",
            '11': "Iconic Dark",
            '12': "Charred Horn",
            '13': "Hot Spring",
            '14': "I Am Fire",
            '15': "Golden PT",
            '18': "Crimson Dawn",
            '1A': "Golden Sunrise",
            '1B': "Golden Sunset",
            '1C': "Firefly",
            '1D': "Obsidian Gold",
            '1E': "Golden Fire"
        },
        "SS": {
            '00': "Random Skin",
            '01': "Melanistic KS",
            '02': "Leucistic KS",
            '03': "Leumelan KS",
            '04': "Crimson PT",
            '05': "Sandslayer",
            '06': "Snowslayer",
            '07': "Melanistic KS19",
            '08': "Leucistic KS19",
            '09': "Leumelan KS19",
            '0A': "Iconic",
            '0B': "Forest Moon",
            '0C': "Galaxy",
            '0D': "Night Sky",
            '0E': "Overo",
            '0F': "Wild Galaxy",
            '10': "Wormhole",
            '11': "Broken Nebula",
            '12': "Starlight",
            '13': "Aurora",
            '14': "Constellation",
            '15': "Northern Lights",
            '16': "Crimson LT",
            '17': "Forest Sky",
            '18': "Painted Sky",
            '19': "Super Nova",
            '1A': "Painted Light",
            '1B': "Golden PT",
            '1C': "Firefly",
            '1D': "Obsidian Gold",
            '1E': "Golden Fire"
        },
        "ASD": {
            '00': "Random Skin",
            '01': "Melanistic KS",
            '02': "Leucistic KS",
            '03': "Leumelan KS",
            '04': "Crimson PT",
            '05': "Sandslayer",
            '06': "Snowslayer",
            '07': "Melanistic KS19",
            '08': "Leucistic KS19",
            '09': "Leumelan KS19",
            '0A': "Iconic",
            '0B': "Iconic Dark",
            '0C': "Dark Forest",
            '0D': "Ginger Piebald",
            '0E': "Overo",
            '0F': "Dark Meadow",
            '10': "Burnt Sky",
            '11': "Toxic",
            '12': "Acid Harvest",
            '13': "Bloodborne",
            '14': "Muddy Drake",
            '15': "Blood Moon",
            '16': "Crimson LT",
            '17': "Tainted",
            '18': "Charred Foliage",
            '19': "Charred Embers",
            '1A': "Jade Walker",
            '1B': "Golden PT",
            '1C': "Firefly",
            '1D': "Obsidian Gold",
            '1E': "Golden Fire"
        }
    }

    role_map = skin_maps.get(role, {})
    skin_hex = f"{saved_skin_index:02X}"
    skin_name = role_map.get(skin_hex, "Unknown Skin")
    print(f"角色{role}的皮肤: {int(skin_hex, 16)} *{skin_name}*")

def output_growth_stage(role, growth_stage):
    """
    输出 Enum_GrowthStage::NewEnumerator 信息，并添加年龄段对照表
    """
    growth_stage_map = {
        1: "Hatchling",
        2: "Juvenile",
        3: "Adult",
        4: "Elder",
        5: "Ancient"
    }
    growth_stage_str = growth_stage_map.get(growth_stage, "Unknown Growth Stage")
    print(f"角色{role}的年龄段: {growth_stage} *{growth_stage_str}*")

def main():
    file_path = get_file_path()

    # 检查文件大小
    try:
        file_size_kb = os.path.getsize(file_path) / 1024
    except Exception as e:
        print(f"错误：无法获取文件大小。详细信息：{e}")
        input("按回车键退出...")
        sys.exit(1)
        
    if file_size_kb >= 29:
        print(f"错误：文件大小为 {file_size_kb:.2f}KB，大于或等于29KB，不符合要求。")
        input("按回车键退出...")
        sys.exit(1)

    # 复制并重命名文件（此处已处理 output 目录不存在的情况）
    copied_file_path = copy_and_rename(file_path)

    # 读取文件内容并转换为HEX
    try:
        with open(copied_file_path, 'rb') as f:
            file_bytes = f.read()
        hex_data = bytes_to_hex(file_bytes)
    except Exception as e:
        print(f"错误：无法读取或转换文件内容。详细信息：{e}")
        input("按回车键退出...")
        sys.exit(1)

    # 查找 "PlayerSteamID"
    player_steam_id_index = find_string(hex_data, "PlayerSteamID")
    if player_steam_id_index == -1:
        print("错误：未找到 'PlayerSteamID' 字符串。")
        input("按回车键退出...")
        sys.exit(1)
    # 计算字符串结束位置
    player_steam_id_end = player_steam_id_index + len("PlayerSteamID") * 2
    # 从 "PlayerSteamID" 后第30个字节开始读取17个字节
    player_steam_id_hex = read_bytes_after(hex_data, player_steam_id_end, 30, 17)
    if not validate_numeric_hex(player_steam_id_hex, expected_length=17, prefix="765611"):
        print("错误：'PlayerSteamID' 后的17个字节不全为数字、长度不符合或不以 '765611' 开头。")
        print(f"读取到的原始HEX值：{format_hex_with_spaces(player_steam_id_hex)}")
        input("按回车键退出...")
        sys.exit(1)
    try:
        player_steam_id = hex_to_bytes(player_steam_id_hex).decode('utf-8')
    except Exception as e:
        print(f"错误：无法解码 'PlayerSteamID'。详细信息：{e}")
        print(f"读取到的原始HEX值：{format_hex_with_spaces(player_steam_id_hex)}")
        input("按回车键退出...")
        sys.exit(1)
    print(f"读取到的 PlayerSteamID: {player_steam_id}")

    # 查找角色相关字符串
    roles = {
        "Enum_PlayerCharacter::NewEnumerator0": "FS",
        "Enum_PlayerCharacter::NewEnumerator2": "SS",
        "Enum_PlayerCharacter::NewEnumerator3": "ASD"
    }
    valid_roles = {}
    for enum_str, role_name in roles.items():
        index = find_string(hex_data, enum_str)
        if index != -1:
            valid_roles[role_name] = index
            print(f"找到有效角色: {role_name}")
        else:
            print(f"未找到角色 {role_name}，跳过。")

    if not valid_roles:
        print("错误：未找到任何有效的角色，结束操作。")
        input("按回车键退出...")
        sys.exit(1)

    print()

    # 存储角色数据
    role_data = {}
    for role, index in valid_roles.items():
        role_info = {}
        # 查找 "SavedGender"
        saved_gender_index = find_string(hex_data[index:], "SavedGender")
        if saved_gender_index == -1:
            print(f"错误：在角色 {role} 中未找到 'SavedGender' 字符串。")
            input("按回车键退出...")
            sys.exit(1)
        # 计算字符串结束位置
        saved_gender_end = saved_gender_index + len("SavedGender") * 2
        # 从 "SavedGender" 后第62个字节开始读取1个字节
        saved_gender_hex = read_bytes_after(hex_data, index + saved_gender_end, 62, 1)
        if not saved_gender_hex:
            print(f"错误：角色 {role} 的 'SavedGender' HEX数据为空。")
            input("按回车键退出...")
            sys.exit(1)
        try:
            saved_gender = int(saved_gender_hex, 16)
            if saved_gender not in [0, 1]:
                print(f"错误：角色 {role} 的 'SavedGender' 值无效 ({saved_gender})。")
                print(f"读取到的 SavedGender HEX值：{format_hex_with_spaces(saved_gender_hex)}")
                input("按回车键退出...")
                sys.exit(1)
            role_info['SavedGender'] = saved_gender
            output_saved_gender(role, saved_gender)
        except:
            print(f"错误：无法解析角色 {role} 的 'SavedGender'。")
            print(f"读取到的 SavedGender HEX值：{format_hex_with_spaces(saved_gender_hex)}")
            input("按回车键退出...")
            sys.exit(1)

        # 查找 "SavedSkinIndex"
        saved_skin_index = find_string(hex_data[index:], "SavedSkinIndex")
        if saved_skin_index == -1:
            print(f"错误：在角色 {role} 中未找到 'SavedSkinIndex' 字符串。")
            input("按回车键退出...")
            sys.exit(1)
        # 计算字符串结束位置
        saved_skin_end = saved_skin_index + len("SavedSkinIndex") * 2
        # 从 "SavedSkinIndex" 后第72个字节开始读取1个字节
        saved_skin_hex = read_bytes_after(hex_data, index + saved_skin_end, 72, 1)
        if not saved_skin_hex:
            print(f"错误：角色 {role} 的 'SavedSkinIndex' HEX数据为空。")
            input("按回车键退出...")
            sys.exit(1)
        try:
            saved_skin = int(saved_skin_hex, 16)
            if not (0 <= saved_skin <= 30):
                print(f"错误：角色 {role} 的 'SavedSkinIndex' 值无效 ({saved_skin})。")
                print(f"读取到的 SavedSkinIndex HEX值：{format_hex_with_spaces(saved_skin_hex)}")
                input("按回车键退出...")
                sys.exit(1)
            role_info['SavedSkinIndex'] = saved_skin
            output_saved_skin_index(role, saved_skin)
        except:
            print(f"错误：无法解析角色 {role} 的 'SavedSkinIndex'。")
            print(f"读取到的 SavedSkinIndex HEX值：{format_hex_with_spaces(saved_skin_hex)}")
            input("按回车键退出...")
            sys.exit(1)

        # 查找 "Enum_GrowthStage::NewEnumerator"
        growth_stage_index = find_string(hex_data[index:], "Enum_GrowthStage::NewEnumerator")
        if growth_stage_index == -1:
            print(f"错误：在角色 {role} 中未找到 'Enum_GrowthStage::NewEnumerator' 字符串。")
            input("按回车键退出...")
            sys.exit(1)
        # 计算字符串结束位置
        growth_stage_end = growth_stage_index + len("Enum_GrowthStage::NewEnumerator") * 2
        # 从 "Enum_GrowthStage::NewEnumerator" 后第0个字节开始读取1个字节
        growth_stage_hex = read_bytes_after(hex_data, index + growth_stage_end, 0, 1)
        if not growth_stage_hex:
            print(f"错误：角色 {role} 的 'Enum_GrowthStage::NewEnumerator' HEX数据为空。")
            input("按回车键退出...")
            sys.exit(1)
        try:
            # 将HEX字节转换为字符，再转换为整数
            growth_stage_char = hex_to_bytes(growth_stage_hex).decode('utf-8')
            growth_stage = int(growth_stage_char)
            if not (1 <= growth_stage <= 5):
                print(f"错误：角色 {role} 的 'Enum_GrowthStage::NewEnumerator' 值无效 ({growth_stage})。")
                print(f"读取到的 Enum_GrowthStage::NewEnumerator HEX值：{format_hex_with_spaces(growth_stage_hex)}")
                input("按回车键退出...")
                sys.exit(1)
            role_info['Enum_GrowthStage'] = growth_stage
            output_growth_stage(role, growth_stage)
            print()
        except:
            print(f"错误：无法解析角色 {role} 的 'Enum_GrowthStage::NewEnumerator'。")
            print(f"读取到的 Enum_GrowthStage::NewEnumerator HEX值：{format_hex_with_spaces(growth_stage_hex)}")
            input("按回车键退出...")
            sys.exit(1)

        role_data[role] = role_info

    # 用户输入部分
    print("所有初始数据读取完毕。")

    # 显示 PlayerSteamID 和有效角色
    print(f"\nPlayerSteamID: {player_steam_id}")
    print("有效角色:")
    for role in valid_roles.keys():
        print(f" - {role}")

    # 修改 PlayerSteamID
    # 新增：记录是否输入了新的 steam64id 用于最终文件重命名
    rename_file = False
    while True:
        new_steam_id = input(f"\n是否要修改 PlayerSteamID？当前值: {player_steam_id}\n请输入新的 PlayerSteamID（或按回车跳过）：").strip()
        if new_steam_id == "":
            print("跳过 PlayerSteamID 的修改。")
            break

        if (len(new_steam_id) == 17 and new_steam_id.isdigit() and new_steam_id.startswith("765611")):
            # 若输入与当前不同，则标记需要重命名文件
            if new_steam_id != player_steam_id:
                player_steam_id = new_steam_id
                rename_file = True
            print(f"PlayerSteamID 已修改为: {player_steam_id}")
            break
        else:
            print("输入无效。PlayerSteamID 必须是17位纯数字，且以 '765611' 开头。请重新输入。")

    # 修改每个角色的属性
    for role in valid_roles.keys():
        print(f"\n开始修改角色: {role}")
        # 修改 SavedGender
        current_gender = role_data[role]['SavedGender']
        while True:
            new_gender = input(f"是否要修改 {role} 的 性别？当前值: {current_gender}\n请输入新的 性别（0=Female, 1=Male，或按回车跳过）：").strip()
            if new_gender == "":
                print("跳过 性别 的修改。\n")
                break
            if new_gender in ['0', '1']:
                new_gender = int(new_gender)
                if new_gender == current_gender:
                    print("输入的值与当前值相同。请重新输入。\n")
                else:
                    role_data[role]['SavedGender'] = new_gender
                    print(f"{role} 的 性别 已修改为: {new_gender}\n")
                    break
            else:
                print("输入无效。性别 必须是 0 或 1。请重新输入。\n")

        # 修改 SavedSkinIndex
        current_skin = role_data[role]['SavedSkinIndex']
        while True:
            new_skin = input(f"是否要修改 {role} 的 皮肤？当前值: {current_skin}\n请输入新的 皮肤（0-30，或按回车跳过）：").strip()
            if new_skin == "":
                print("跳过 皮肤 的修改。\n")
                break
            if new_skin.isdigit():
                new_skin = int(new_skin)
                if 0 <= new_skin <= 30:
                    if new_skin == current_skin:
                        print("输入的值与当前值相同。请重新输入。\n")
                    else:
                        role_data[role]['SavedSkinIndex'] = new_skin
                        print(f"{role} 的 皮肤 已修改为: {new_skin}\n")
                        break
                else:
                    print("输入无效。皮肤 必须在 0 到 30 之间。请重新输入。\n")
            else:
                print("输入无效。皮肤 必须是数字。请重新输入。\n")

        # 修改 Enum_GrowthStage::NewEnumerator
        current_growth = role_data[role]['Enum_GrowthStage']
        while True:
            new_growth = input(f"是否要修改 {role} 的 年龄段？当前值: {current_growth}\n请输入新的值（1-5，或按回车跳过）：").strip()
            if new_growth == "":
                print("跳过 年龄段 的修改。\n")
                break
            if new_growth.isdigit():
                new_growth_int = int(new_growth)
                if 1 <= new_growth_int <= 5:
                    if new_growth_int == current_growth:
                        print("输入的值与当前值相同。请重新输入。\n")
                    else:
                        role_data[role]['Enum_GrowthStage'] = new_growth_int
                        print(f"{role} 的 年龄段 已修改为: {new_growth_int}\n")
                        break
                else:
                    print("输入无效。年龄段 必须在 1 到 5 之间。请重新输入。\n")
            else:
                print("输入无效。年龄段 必须是数字。请重新输入。\n")

    # 显示所有修改内容
    print("\n所有修改已完成。以下是修改后的内容与原始内容的对比：")
    print(f"\nPlayerSteamID: {player_steam_id}")
    print("有效角色:")
    for role in valid_roles.keys():
        print(f" - {role}")
    for role, info in role_data.items():
        print(f"\n角色: {role}")
        print(f"  性别: {info['SavedGender']}")
        print(f"  皮肤: {info['SavedSkinIndex']}")
        print(f"  年龄段: {info['Enum_GrowthStage']}")

    # 更新HEX数据
    # 修改 PlayerSteamID
    player_steam_id_bytes = player_steam_id.encode('utf-8')
    player_steam_id_hex_new = bytes_to_hex(player_steam_id_bytes)
    try:
        # 计算字符串结束位置
        player_steam_id_end = player_steam_id_index + len("PlayerSteamID") * 2
        # 更新HEX数据
        hex_data = (
            hex_data[:player_steam_id_end + 30 * 2] +
            player_steam_id_hex_new +
            hex_data[player_steam_id_end + 30 * 2 + 17 * 2:]
        )
    except Exception as e:
        print(f"错误：无法更新 'PlayerSteamID'。详细信息：{e}")
        print(f"尝试替换的HEX位置：从索引 {player_steam_id_end + 30 * 2} 开始，长度17个字节。")
        input("按回车键退出...")
        sys.exit(1)

    # 修改每个角色的属性
    for role, info in role_data.items():
        index = valid_roles[role]
        # 修改 SavedGender
        saved_gender_index = find_string(hex_data[index:], "SavedGender")
        if saved_gender_index != -1:
            # 计算字符串结束位置
            saved_gender_end = saved_gender_index + len("SavedGender") * 2
            absolute_index = index + saved_gender_end + 62 * 2
            try:
                hex_data = (
                    hex_data[:absolute_index] +
                    f"{info['SavedGender']:02X}" +
                    hex_data[absolute_index + 2:]
                )
            except Exception as e:
                print(f"错误：无法更新 {role} 的 'SavedGender'。详细信息：{e}")
                print(f"尝试替换的HEX位置：索引 {absolute_index}。")
                print(f"当前角色属性：SavedGender={info['SavedGender']}")
                input("按回车键退出...")
                sys.exit(1)

        # 修改 SavedSkinIndex
        saved_skin_index = find_string(hex_data[index:], "SavedSkinIndex")
        if saved_skin_index != -1:
            # 计算字符串结束位置
            saved_skin_end = saved_skin_index + len("SavedSkinIndex") * 2
            absolute_index = index + saved_skin_end + 72 * 2
            try:
                hex_data = (
                    hex_data[:absolute_index] +
                    f"{info['SavedSkinIndex']:02X}" +
                    hex_data[absolute_index + 2:]
                )
            except Exception as e:
                print(f"错误：无法更新 {role} 的 'SavedSkinIndex'。详细信息：{e}")
                print(f"尝试替换的HEX位置：索引 {absolute_index}。")
                print(f"当前角色属性：SavedSkinIndex={info['SavedSkinIndex']}")
                input("按回车键退出...")
                sys.exit(1)

        # 修改 Enum_GrowthStage::NewEnumerator
        growth_stage_index = find_string(hex_data[index:], "Enum_GrowthStage::NewEnumerator")
        if growth_stage_index != -1:
            # 计算字符串结束位置
            growth_stage_end = growth_stage_index + len("Enum_GrowthStage::NewEnumerator") * 2
            absolute_index = index + growth_stage_end + 0 * 2  # 偏移0个字节
            try:
                # 将整数1-5转换为对应的ASCII字符'1'-'5', 然后转换为HEX
                growth_stage_char = str(info['Enum_GrowthStage'])
                growth_stage_hex_new = bytes_to_hex(growth_stage_char.encode('utf-8'))
                hex_data = (
                    hex_data[:absolute_index] +
                    growth_stage_hex_new +
                    hex_data[absolute_index + 2:]
                )
            except Exception as e:
                print(f"错误：无法更新 {role} 的 'Enum_GrowthStage::NewEnumerator'。详细信息：{e}")
                print(f"尝试替换的HEX位置：索引 {absolute_index}。")
                print(f"当前角色属性：Enum_GrowthStage::NewEnumerator={info['Enum_GrowthStage']}")
                input("按回车键退出...")
                sys.exit(1)

    # 将修改后的HEX数据写回文件
    try:
        new_file_bytes = hex_to_bytes(hex_data)
    except binascii.Error:
        print("错误：修改后的HEX数据无效，无法转换回字节。")
        print(f"修改后的HEX数据长度：{len(hex_data)}")
        input("按回车键退出...")
        sys.exit(1)
    except Exception as e:
        print(f"错误：无法转换HEX数据为字节。详细信息：{e}")
        input("按回车键退出...")
        sys.exit(1)

    try:
        with open(copied_file_path, 'wb') as f:
            f.write(new_file_bytes)
        print(f"\n所有修改已写入文件: {copied_file_path}")
    except Exception as e:
        print(f"错误：无法写入修改后的数据到文件。详细信息：{e}")
        input("按回车键退出...")
        sys.exit(1)

    # 新增：如果用户输入了新的 PlayerSteamID，则重命名修改后的存档文件
    if rename_file:
        directory = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(directory, "output")
        new_file_name = f"{player_steam_id}.sav"
        new_file_path = os.path.join(output_dir, new_file_name)
        try:
            os.rename(copied_file_path, new_file_path)
            print(f"\n文件已重命名为: {new_file_name}")
        except Exception as e:
            print(f"错误：无法重命名文件。详细信息：{e}")
            input("按回车键退出...")
            sys.exit(1)

    # 处理完成后暂停
    input("处理完成。按回车键退出...")

if __name__ == "__main__":
    main()
