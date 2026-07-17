import tkinter as tk
import winsound  # WindowsのBeep音を鳴らすため

class ClipboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("現在の文字数: 0")
        self.root.geometry("770x550")
        
        # 内部データの初期化
        self.cb_old = ""
        self.all_text = ""
        
        # 画面の作成
        self.create_widgets()
        
        # クリップボードを空にして監視を開始
        self.clear_clipboard()
        self.monitor_clipboard()

    def create_widgets(self):
        # 左側のボタン配置用フレーム
        btn_frame = tk.Frame(self.root)
        btn_frame.place(x=10, y=10, width=120, height=530)
        
        # ボタンの作成
        btn_copy     = tk.Button(btn_frame, text="copy", command=self.action_copy)
        btn_restart  = tk.Button(btn_frame, text="restart", command=self.action_restart)
        btn_chk_up   = tk.Button(btn_frame, text="chk up", command=self.action_tmp)
        btn_chk_down = tk.Button(btn_frame, text="chk down", command=self.action_tmp)
        btn_clear    = tk.Button(btn_frame, text="clear", command=self.action_clear)
        btn_copy_all = tk.Button(btn_frame, text="copy ALL", command=self.action_copy_all)
        
        # ボタンを上から順番に配置
        buttons = [btn_copy, btn_restart, btn_chk_up, btn_chk_down, btn_clear, btn_copy_all]
        for btn in buttons:
            btn.pack(fill=tk.X, pady=5, ipady=2)

        # 右側のテキスト入力欄
        # 上の入力欄 (var4mesbox_Aに相当)
        self.txt_A = tk.Text(self.root, undo=True, font=("MS Gothic", 10))
        self.txt_A.place(x=140, y=10, width=620, height=200)
        
        # 下の入力欄 (var4mesbox_Bに相当)
        self.txt_B = tk.Text(self.root, undo=True, font=("MS Gothic", 10))
        self.txt_B.place(x=140, y=220, width=620, height=300)

    def monitor_clipboard(self):
        """クリップボードを定期的に監視する処理"""
        try:
            # クリップボードから文字列の取得を試みる
            cb_new = self.root.clipboard_get()
        except tk.TclError:
            # クリップボードが空、または画像などのテキスト以外が入っている場合は無視する
            cb_new = ""
            
        if cb_new and cb_new != self.cb_old:
            # 新しいテキストがコピーされたら処理を実行
            self.action_copy(cb_new)
            
        # 50ミリ秒後に再度この関数を実行する（無限ループの代わり）
        self.root.after(50, self.monitor_clipboard)

    def action_copy(self, text_to_copy=None):
        """新しいコピーを検知したときの処理"""
        # 監視経由ではなく手動でボタンを押された場合は、上の入力欄Aの中身を取得する
        if text_to_copy is None:
            text_to_copy = self.txt_A.get("1.0", tk.END).strip()
            if not text_to_copy:
                return

        # 蓄積用テキストの末尾に新テキストを追加して、間を2行改行する
        self.all_text += text_to_copy + "\n\n"
        self.cb_old = text_to_copy
        
        # 画面の更新（上の入力欄A）
        self.txt_A.delete("1.0", tk.END)
        self.txt_A.insert("1.0", text_to_copy)
        
        # 画面の更新（下の入力欄B：常に末尾に追加）
        self.txt_B.delete("1.0", tk.END)
        self.txt_B.insert("1.0", self.all_text)
        
        # 下の入力欄Bを自動で一番下までスクロールさせる
        self.txt_B.see(tk.END)
        
        # タイトルの文字数を更新
        self.root.title(f"現在の文字数: {len(self.all_text)}")
        
        # 成功音 (1000Hzで500ミリ秒)
        try:
            winsound.Beep(1000, 500)
        except Exception:
            pass

    def action_clear(self):
        """全初期化"""
        self.clear_clipboard()
        self.all_text = ""
        self.cb_old = ""
        
        self.txt_A.delete("1.0", tk.END)
        self.txt_B.delete("1.0", tk.END)
        self.root.title("現在の文字数: 0")
        
        try:
            winsound.Beep(1000, 500)
        except Exception:
            pass

    def action_copy_all(self):
        """下の入力欄Bの内容を、上の入力欄Aとクリップボードに同期する"""
        content_B = self.txt_B.get("1.0", tk.END).rstrip("\n")
        
        self.txt_A.delete("1.0", tk.END)
        self.txt_A.insert("1.0", content_B)
        
        self.clear_clipboard()
        self.root.clipboard_append(content_B)
        self.cb_old = content_B
        
        try:
            winsound.Beep(1000, 500)
        except Exception:
            pass

    def action_restart(self):
        """再起動の代わり（クリップボードを空にしてリセット）"""
        self.clear_clipboard()
        self.cb_old = ""

    def action_tmp(self):
        """chk up / chk down 用の予備の処理"""
        pass

    def clear_clipboard(self):
        """クリップボードの初期化"""
        try:
            self.root.clipboard_clear()
        except Exception:
            pass

# アプリの起動
if __name__ == "__main__":
    app_root = tk.Tk()
    app = ClipboardApp(app_root)
    app_root.mainloop()
