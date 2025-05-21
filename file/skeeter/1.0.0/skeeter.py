#WELCOME TO SKEETER SOURCE CODE!!
#DISCORD JOIN PLEASE!
#AND UPDATE NOTICE HERE
#https://discord.gg/3R7sRvRzxU

import scratchattach as scratch3
import os
import time
import random
import string
import requests
import json
from colorama import Fore, Style, init
from bs4 import BeautifulSoup

# 初期化
init()

# 新ロゴ
logo = r"""
  _____ _  ________ ______ _______ ______ _____  
 / ____| |/ /  ____|  ____|__   __|  ____|  __ \
| (___ | ' /| |__  | |__     | |  | |__  | |__) |
 \___ \|  < |  __| |  __|    | |  |  __| |  _  / 
 ____) | . \| |____| |____   | |  | |____| | \ \ 
|_____/|_|\_\______|______|  |_|  |______|_|  \_\

"""

# 状態管理
accounts = {}
active_account = None
sessions = {}
jump_target = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def blinking_cursor():
    return '|' if int(time.time() * 2) % 2 == 0 else ' '

def save_accounts():
    try:
        with open("login.txt", "w") as f:
            json.dump(accounts, f)
    except Exception as e:
        print(Fore.RED + f"[エラー] login.txt に保存できません: {e}" + Style.RESET_ALL)


def load_accounts():
    global accounts, sessions, active_account
    if os.path.exists("login.txt"):
        with open("login.txt", "r") as f:
            try:
                accounts = json.load(f)
                for username, password in accounts.items():
                    try:
                        sessions[username] = scratch3.login(username, password)
                        if not active_account:
                            active_account = username
                    except:
                        pass
            except:
                accounts = {}

def title_screen():
    global jump_target
    while True:
        clear()
        print(logo)
        print()
        print("[1]Login   [2]Logout   [3]Jump Page   [4]Comment")
        print("[5]Auto Like   [6]Account   [7]Change Account")
        print("[8]Add Studio   [9]Search   [10]Exit")
        print()
        print(f"Active: {active_account if active_account else 'None'}")
        print(blinking_cursor(), end="\r")
        time.sleep(0.5)

        if os.name == "nt":
            import msvcrt
            input_buffer = ""
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode()
                    if key.isdigit():
                        input_buffer += key
                        print(key, end="", flush=True) # 入力された数字を表示
                    elif key == '\r':
                        print() # 改行
                        if input_buffer == '1':
                            login()
                        elif input_buffer == '2':
                            logout()
                        elif input_buffer == '3':
                            jump_page()
                        elif input_buffer == '4':
                            comment()
                        elif input_buffer == '5':
                            auto_like()
                        elif input_buffer == '6':
                            show_accounts()
                        elif input_buffer == '7':
                            change_account()
                        elif input_buffer == '8':
                            add_studio()
                        elif input_buffer == '9':
                            search_projects()
                        elif input_buffer == '10':
                            exit_program()
                        input_buffer = "" # 処理後にバッファをクリア
                        break # Enterが押されたら内側のループを抜ける
                    elif key == '\x08': # Backspaceキー
                        if input_buffer:
                            input_buffer = input_buffer[:-1]
                            print("\b \b", end="", flush=True) # カーソルを戻してスペースで消す
                time.sleep(0.05) # 少し待つことでCPU負荷を軽減

def login():
    global active_account
    clear()
    print("Name:", end=" ")
    username = input()
    print("Pass:", end=" ")
    password = input()

    try:
        session = scratch3.login(username, password)
        accounts[username] = password
        sessions[username] = session
        active_account = username
        save_accounts()
        print(Fore.CYAN + f"\nLogin Success" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nLogin Failed: {e}" + Style.RESET_ALL)

    input("\nEnterで戻る")

def logout():
    global active_account
    if active_account in accounts:
        del accounts[active_account]
        del sessions[active_account]
        active_account = None if not accounts else next(iter(accounts))
        save_accounts()
    print(Fore.CYAN + "\nLogged out." + Style.RESET_ALL)
    input("\nEnterで戻る")

def jump_page():
    global jump_target
    clear()
    print("ジャンプ先を入力（project:ID user:USERNAME studio:ID）")
    jump_target = input(">> ")
    print(Fore.CYAN + "\nJump Success: " + jump_target + Style.RESET_ALL)
    input("\nEnterで戻る")

def comment():
    global jump_target
    clear()
    if not active_account:
        print(Fore.RED + "※ログインが必要です。" + Style.RESET_ALL)
        input("\nEnterで戻る")
        return

    if not jump_target:
        print(Fore.RED + "※ジャンプ先を設定してください。" + Style.RESET_ALL)
        input("\nEnterで戻る")
        return

    count = int(input("Count (送信回数 5〜10 推奨): "))
    content = input("Comment: ")
    use_random = input("Random text [Y/N]: ").strip().lower() == "y"

    delay = 10

    targets = sessions.items() if active_account == "ALL" else [(active_account, sessions[active_account])]

    for username, session in targets:
        print(Fore.YELLOW + f"\n--- {username} の操作を開始 ---" + Style.RESET_ALL)
        try:
            if jump_target.startswith("project:"):
                project_id = jump_target.split(":")[1]
                project = session.connect_project(project_id)
                for i in range(count):
                    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=5)) if use_random else ""
                    project.post_comment(content + (" " + suffix if suffix else ""))
                    print(Fore.GREEN + f"[{i+1}] Comment sent" + Style.RESET_ALL)
                    time.sleep(delay)
            elif jump_target.startswith("user:"):
                username_target = jump_target.split(":")[1]
                user = session.connect_user(username_target)
                for i in range(count):
                    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=5)) if use_random else ""
                    user.post_comment(content + (" " + suffix if suffix else ""))
                    print(Fore.GREEN + f"[{i+1}] Comment sent" + Style.RESET_ALL)
                    time.sleep(delay)
        except Exception as e:
            print(Fore.RED + f"エラー ({username}): {e}" + Style.RESET_ALL)

    input("\nEnterで戻る")

def auto_like():
    clear()
    if not active_account:
        print(Fore.RED + "※ログインが必要です。" + Style.RESET_ALL)
        input("\nEnterで戻る")
        return

    if not jump_target or not jump_target.startswith("project:"):
        print(Fore.RED + "※ジャンプ先は project:ID の形式にしてください。" + Style.RESET_ALL)
        input("\nEnterで戻る")
        return

    targets = sessions.items() if active_account == "ALL" else [(active_account, sessions[active_account])]
    project_id = jump_target.split(":")[1]

    for username, session in targets:
        try:
            project = session.connect_project(project_id)
            project.love()
            project.favorite()
            print(Fore.GREEN + f"♥ {username} が Like しました。" + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"{username} エラー: {e}" + Style.RESET_ALL)

    input("\nEnterで戻る")

def show_accounts():
    clear()
    print("ログイン中アカウント一覧：\n")
    for i, name in enumerate(accounts.keys(), 1):
        print(f"[{i}] {name}" + (" (Active)" if name == active_account else ""))
    input("\nEnterで戻る")

def change_account():
    global active_account
    clear()
    print("切り替えるアカウント番号を入力（全アカウントで操作したい場合は 'All' と入力）：\n")
    for i, name in enumerate(accounts.keys(), 1):
        print(f"[{i}] {name}")
    choice = input("\n>> ").strip()

    if choice.lower() == "all":
        confirm = input(Fore.YELLOW + "\n操作をログイン中のアカウント全てで行うため危険性があります\n実行しますか？ y/n: " + Style.RESET_ALL).strip().lower()
        if confirm == "y":
            active_account = "ALL"
            print(Fore.CYAN + "\nすべてのアカウントでの操作モードに切り替えました。" + Style.RESET_ALL)
        else:
            print(Fore.RED + "\nキャンセルされました。" + Style.RESET_ALL)
    else:
        try:
            idx = int(choice) - 1
            selected = list(accounts.keys())[idx]
            active_account = selected
            print(Fore.CYAN + f"\nActive Account: {selected}" + Style.RESET_ALL)
        except:
            print(Fore.RED + "\n無効な番号です。" + Style.RESET_ALL)
    input("\nEnterで戻る")

def exit_program():
    clear()
    print(Fore.YELLOW + "終了します。" + Style.RESET_ALL)
    exit()

def add_studio():
    clear()
    if not active_account or not jump_target.startswith("studio:"):
        print(Fore.RED + "※studio:ID にジャンプしてから実行してください。" + Style.RESET_ALL)
        input("\nEnterで戻る")
        return

    studio_id = jump_target.split(":")[1]
    session = sessions[active_account]
    studio = session.connect_studio(studio_id)

    if not os.path.exists("list.txt"):
        print("list.txt が見つかりません。")
        input("\nEnterで戻る")
        return

    with open("list.txt", "r") as f:
        urls = list(set([line.strip() for line in f if line.strip()]))

    existing_projects = [project.id for project in studio.projects()]

    for url in urls:
        try:
            if "/projects/" in url:
                pid = url.split("/projects/")[1].split("/")[0]
                if pid in existing_projects:
                    print(f"スキップ（既に追加済）: {pid}")
                    continue
                studio.add_project(pid)
                print(f"追加成功: {pid}")
                time.sleep(random.uniform(10, 15))
        except Exception as e:
            print(f"追加失敗: {e}")

    input("\nEnterで戻る")

def search_projects():
    clear()
    print("検索ワードを入力（例：柴田理恵 page:1）")
    query = input(">> ")

    if "page:" in query:
        keyword, page = query.split("page:")
        page = int(page.strip())
        keyword = keyword.strip()
    else:
        keyword = query.strip()
        page = 1

    url = f"https://api.scratch.mit.edu/search/projects?q={keyword}&mode=trending&limit=40&offset={(page - 1) * 40}"

    try:
        res = requests.get(url).json()
        new_urls = set()
        for project in res:
            pid = project.get("id")
            if pid:
                new_urls.add(f"https://scratch.mit.edu/projects/{pid}/")
                print(f"追加予定: {pid}")
                time.sleep(random.uniform(1, 2))

        if not os.path.exists("list.txt"):
            existing_urls = set()
        else:
            with open("list.txt", "r") as f:
                existing_urls = set(line.strip() for line in f if line.strip())

        with open("list.txt", "a") as f:
            for url in sorted(new_urls - existing_urls):
                f.write(url + "\n")
                print(f"保存済: {url}")

    except Exception as e:
        print(f"検索エラー: {e}")

    input("\nEnterで戻る")


if __name__ == "__main__":
    load_accounts()
    title_screen()
