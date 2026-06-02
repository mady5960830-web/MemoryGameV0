import tkinter as tk
from tkinter import messagebox
import random
import time


####################################
# Card 類別
# 繼承 Button
####################################

class Card(tk.Button):

    def __init__(self,
                 master,
                 value,
                 game,
                 **kwargs):

        super().__init__(
            master,
            width=8,
            height=4,
            font=("Arial",16),
            command=self.click_card,
            **kwargs
        )

        self.value=value
        self.game=game

        self.is_flipped=False
        self.is_matched=False

        self.show_back()


    ##############################

    def show_back(self):

        if not self.is_matched:

            self.config(
                text="❓",
                state="normal"
            )

            self.is_flipped=False


    ##############################

    def show_front(self):

        self.config(
            text=self.value
        )

        self.is_flipped=True


    ##############################

    def clear_card(self):

        self.config(
            text="",
            state="disabled",
            bg="lightgray"
        )

        self.is_matched=True


    ##############################

    def click_card(self):

        self.game.select_card(self)



####################################
# Game
####################################

class MemoryGame:

    def __init__(self,root):

        self.root=root

        self.root.title(
            "翻牌記憶遊戲, author: S1141388 蒲美蓁"
        )

        self.root.geometry(
            "700x520"
        )

        ########################

        self.first_card=None
        self.second_card=None

        self.lock=False

        self.start_time=time.time()

        ########################
        # 上方資訊
        ########################

        top_frame=tk.Frame(root)

        top_frame.pack()

        self.time_label=tk.Label(
            top_frame,
            text="時間:0 秒",
            font=("Arial",16)
        )

        self.time_label.pack()

        ########################
        # 卡片區
        ########################

        self.frame=tk.Frame(root)

        self.frame.pack()

        self.create_cards()

        self.update_timer()


    ################################

    def create_cards(self):

        cards=[
            "A","2","3","4",
            "5","6","7","8",
            "9","10","J","Q"
        ]

        cards=cards*2

        random.shuffle(cards)

        self.card_list=[]

        index=0

        for r in range(4):

            for c in range(6):

                card=Card(
                    self.frame,
                    cards[index],
                    self
                )

                card.grid(
                    row=r,
                    column=c,
                    padx=5,
                    pady=5
                )

                self.card_list.append(
                    card
                )

                index+=1


    ################################
    # 點牌
    ################################

    def select_card(self,card):

        if self.lock:
            return

        if card.is_flipped:
            return

        if card.is_matched:
            return


        card.show_front()


        ########################

        if self.first_card is None:

            self.first_card=card

            return


        ########################

        self.second_card=card

        self.lock=True

        self.root.after(
            3000,
            self.check_match
        )


    ################################
    # 檢查配對
    ################################

    def check_match(self):

        if (
            self.first_card.value
            ==
            self.second_card.value
        ):

            self.first_card.clear_card()

            self.second_card.clear_card()

        else:

            self.first_card.show_back()

            self.second_card.show_back()


        self.first_card=None

        self.second_card=None

        self.lock=False

        self.check_game_finish()


    ################################
    # 是否過關
    ################################

    def check_game_finish(self):

        finished=True

        for card in self.card_list:

            if not card.is_matched:

                finished=False
                break


        if finished:

            elapsed=int(
                time.time()
                -self.start_time
            )

            result=messagebox.askyesno(
                "遊戲完成",
                f"恭喜過關！\n"
                f"花費:{elapsed}秒\n"
                f"重新開始?"
            )

            if result:

                self.restart()

            else:

                self.root.destroy()


    ################################
    # 計時器
    ################################

    def update_timer(self):

        elapsed=int(
            time.time()
            -self.start_time
        )

        self.time_label.config(
            text=f"時間:{elapsed} 秒"
        )

        if not self.is_finished():

            self.root.after(
                1000,
                self.update_timer
            )


    ################################

    def is_finished(self):

        for card in self.card_list:

            if not card.is_matched:

                return False

        return True


    ################################
    # 重置遊戲
    ################################

    def restart(self):

        self.frame.destroy()

        self.frame=tk.Frame(
            self.root
        )

        self.frame.pack()

        self.start_time=time.time()

        self.first_card=None
        self.second_card=None
        self.lock=False

        self.create_cards()

        self.update_timer()



####################################

root=tk.Tk()

game=MemoryGame(root)

root.mainloop()