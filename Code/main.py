import sys
from UI import window
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.QtGui import QPainter
import time


# 用于在分数统计中显示各项细节分数, 记录得分项名称和分值
class temp_score(QListWidgetItem):

    def __init__(self, name, value, parent=None):
        val = str(name) + "(" + str(value) + ")"
        super(temp_score, self).__init__(val)
        self.name = name
        self.value = value


class main_window(QMainWindow, window.Ui_MainWindow):

    def __init__(self, parent=None):
        super(main_window, self).__init__(parent)
        self.setupUi(self)
        self.finalScore = 0

    # team_score = [0, 20, 60, 80, 100, 150, 250]
    # boss加分
    # 3层boss， 无隐藏， 呼吸， 夺树者， 大地醒转
    mid_boss = [0, 50, 50, 10]
    # 5层boss， 未通过， 一结局， 二结局
    ending_1_score = [0, 100, 150]
    # 6层boss， 未通过， 1+3， 2+3
    ending_2_score = [0, 50, 350]

    # end_board_score = [0, 50, 50, 100]
    # end_ex_score = [0, 0, 0, 250]

    # 计算当前列表得分
    def calculate_temp(self):
        name = self.id.text()

        final_score = 0
        for _ in range(self.list_score.count()):
            final_score += self.list_score.item(_).value

        self.finalScore = final_score
        self.label_show.setText('选手: ' + name + '\n最终得分: ' + str(final_score))

    # 一键算分
    def calculate(self):
        origin_score = self.origin_score.value()
        self.add_item("结算分", origin_score)

        # 加上分队补正
        # team_list = []
        # team_list.append(self.st_1)
        # team_list.append(self.st_2)
        # team_list.append(self.st_3)
        # team_list.append(self.st_4)
        # team_list.append(self.st_5)
        # team_list.append(self.st_6)
        # team_list.append(self.st_7)

        # for si in range(7):
        #     if team_list[si].isChecked():
        #         self.add_item(team_list[si].text(), self.team_score[si])

        # 减去存款限制
        delta = self.coin_init.value() - self.coin_final.value()
        delta -= 60

        if delta > 0:
            self.add_item("取款超额", -1 * delta * 50)

        # 加上3层boss加分
        b_list = [self.b_0, self.b_1, self.b_2, self.b_3]
        for bi in range(len(b_list)):
            if b_list[bi].isChecked():
                self.add_item(b_list[bi].text(), self.mid_boss[bi])
                break

        # 加上结局分数修正
        # 未通关， 1结局， 2结局
        ending5_list = [self.end_0, self.end_1, self.end_2]
        for ei in range(3):
            if ending5_list[ei].isChecked():
                end_name = ending5_list[ei].text()
                end_value = self.ending_1_score[ei]
                # 5层无密文板
                if self.ex_b_1.isChecked():
                    end_name = end_name + "|无加成"
                    end_value += 50
                # 通关园丁
                if self.end_3.isChecked():
                    end_name = end_name + "+" + self.end_3.text()
                    end_value += self.ending_2_score[ei]
                    # 6层无密文板
                    if self.ex_b_2.isChecked():
                        end_name = end_name + "|无加成"
                        end_value += 50
                    # 技术补正
                    if ei == 2 and self.ex_t.isChecked():
                        end_name = end_name + "|技术补正"
                        end_value += 300
                self.add_item(end_name, end_value)
                break

        # 临时干员加分
        c6 = self.cb_6.value()
        if c6 > 0:
            self.add_item("六星干员" + ":" + str(c6), int(50 * c6))

        c5 = self.cb_5.value()
        if c5 > 0:
            self.add_item("五星干员" + ":" + str(c5), int(20 * c5))

        c4 = self.cb_4.value()
        if c4 > 0:
            self.add_item("四星干员" + ":" + str(c4), int(10 * c4))

        # 鸭狗熊加分
        n1 = self.n_duck.value()
        if n1 > 0:
            self.add_item("鸭" + ":" + str(n1), int(20 * n1))

        n2 = self.n_dog.value()
        if n2 > 0:
            self.add_item("狗" + ":" + str(n2), int(20 * n2))

        n3 = self.n_bear.value()
        if n3 > 0:
            self.add_item("熊" + ":" + str(n3), int(20 * n3))

        # 藏品修正
        n4 = self.n_collection.value()
        self.add_item("藏品和道具" + ":" + str(n4), int(10 * n4))

        # 密文板数量修正
        n5 = self.n_board.value()
        self.add_item("密文板" + ":" + str(n5), int(5 * n5))

        self.calculate_temp()


    # 重置作战加分项
    def clear(self):
        # self.origin_score.setValue(0)

        # self.st_1.setChecked(True)
        # self.st_1.setAutoExclusive(False)
        # self.st_1.setChecked(False)
        # self.st_1.setAutoExclusive(True)

        # self.b_0.setChecked(True)

        # self.end_0.setChecked(True)

        # self.ex_2.setChecked(False)
        # self.ex_b.setChecked(False)

        # self.ch_1.setCurrentIndex(0)
        self.em_1.setCurrentIndex(0)
        self.hd_1.setCurrentIndex(0)

        # self.ch_a.setChecked(False)
        self.em_a.setChecked(False)
        self.em_b.setChecked(False)
        self.em_c.setChecked(False)
        self.em_d.setChecked(False)
        self.hd_a.setChecked(False)
        self.hd_b.setChecked(False)

        self.hd_hero.setValue(0)
        self.hd_justice.setValue(0)
        # self.n_duck.setValue(0)
        # self.n_dog.setValue(0)
        # self.n_bear.setValue(0)
        # self.n_collection.setValue(0)
        # self.n_board.setValue(0)

        # self.ch_name.setText("")
        # self.finalScore = 0

    # 重置(重新生成界面)
    def clean(self):
        px = self.width()
        py = self.height()
        self.setupUi(self)
        self.tn = []
        self.finalScore = 0
        self.resize(px, py)

    # 临时干员加分
    # ch_score = [50, 20, 10]
    # def add_ch(self):
    #     name = ""
    #     if self.ch_name.text() is not None and self.ch_name.text() != "":
    #         name = self.ch_name.text()
    #     else:
    #         name = self.ch_1.currentText()

    #     value = self.ch_score[self.ch_1.currentIndex()]

    #     if self.ch_a.isChecked():
    #         name = name + "|密文板"
    #         value = int(value / 2)

    #     self.add_item(name, value)

    # 紧急作战加分
    # 普通紧急，冰海，狡兽，午后，公司，禁区，本能，亡者，乐理，表象，山海，求敌，生人，生灵，霜与沙
    # 基础得分
    # 普通紧急
    em_score = [0, 
                # 冰海，狡兽
                40, 20, 
                # 午后，公司，禁区
                40, 40, 20, 
                # 本能，亡者，乐理，表象，山海，求敌，生人
                120, 120, 80, 80, 70, 60, 40, 
                # 生灵，霜与沙
                150, 70]
    # 无漏加分
    em_ex_score = [0, 
                   20, 0, 
                   0, 20, 0, 
                   0, 20, 20, 0, 0, 0, 0, 
                   0, 0]

    def add_em(self):
        name = self.em_1.currentText()
        index = self.em_1.currentIndex()
        # 加上基础得分
        value = self.em_score[index]

        # 加上无漏加分
        if self.em_a.isChecked():
            name = name + "|无漏"
            value += self.em_ex_score[index]

        # 加上路网补正
        if self.em_b.isChecked():
            # 除6层紧急，加分
            if index < 13:
                name = name + "|路网"
                value += 10
        # 加上树篱补正
        if self.em_c.isChecked():
            # 除普通紧急，加分
            if index > 0:
                name = name + "|树篱"
                value += 20
        # 加上冰海或乐理的特殊加分
        if self.em_d.isChecked():
            if index == 1:
                name = name + "|大量坍缩体"
                value += 10
            elif index == 8:
                name = name + "|第四位术士"
                value += 20

        self.add_item(name, value)

    # 隐藏作战加分
    # 豪华车队，正义使者， 英雄无名
    hd_score = [20, 70, 30]
    # 无漏加分
    hd_ex_score = [0, 40, 30]

    def add_ex(self):
        name = self.hd_1.currentText()
        index = self.hd_1.currentIndex()
        # 加上通关关卡得分
        value = self.hd_score[index]

        # 如果为豪华车队或正义使者
        if index != 2:
            # 加上击杀隐藏敌人分，每名30
            if self.hd_justice.value() > 0:
                t = self.hd_justice.value()
                if index == 0:
                    name = name + "|击杀熊"
                    t = 1
                else:
                    name = name + "|收隐藏" + str(t)
                value = value + t * 30

        # 如果为英雄无名
        else:
            # 加上击杀敌人分，每名15
            if self.hd_hero.value() > 0:
                value = value + self.hd_hero.value() * 15
            # 击杀6名说明无漏
            if self.hd_hero.value() == 6:
                self.hd_a.setChecked(True)

        # 加上无漏得分
        if self.hd_a.isChecked():
            name = name + "|无漏"
            value += self.hd_ex_score[index]

        # 加上树篱补正
        if self.hd_b.isChecked():
            name = name + "|树篱"
            value += 20

        self.add_item(name, value)

    # 选择所有临时分数项
    def select_all(self):
        self.list_score.selectAll()

    # tn为暂存的被删除数据队列
    tn = []

    # 删除选择数据进入tn暂存
    def del_select(self):
        # t为所选的删除数据
        t = []
        selected_items = self.list_score.selectedItems()
        for item in selected_items:
            t.append(self.list_score.takeItem(self.list_score.row(item)))
        self.tn.append(t)

    # 撤回保存在tn队列的被删除数据,按照出栈规则
    def withdraw(self):
        # t为恢复的数据，位于tn栈顶
        t = None
        if len(self.tn) > 0:
            t = self.tn.pop()
        if t is not None:
            for ti in t:
                self.list_score.addItem(ti)

    # 初始化图像渲染，产生截图并保存
    def output(self):
        painter = QPainter(self)
        pixmap = QApplication.primaryScreen().grabWindow(self.winId())
        painter.drawPixmap(0, 0, pixmap)
        self.save_screenshot(pixmap)

    # 产生并保存截图，附带选手和得分信息，以及时间戳，方便区分
    def save_screenshot(self, pixmap):
        timestamp = time.time()
        # 命名规则为 screenshot + 选手id + 选手得分 + 时间戳
        pic_name = "screenshot" + "_" + str(self.id.text()) + "_" + str(
            self.finalScore) + "_" + str(int(timestamp)) + ".png"
        if pixmap.save(pic_name):
            QMessageBox.information(self, 'Screenshot',
                                    'Screenshot saved successfully!')
        else:
            QMessageBox.warning(self, 'Screenshot',
                                'Failed to save screenshot!')
        pass

    # 添加临时加分项（名称，分值）
    def add_item(self, name, value):
        item = temp_score(name, value)
        self.list_score.addItem(item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = main_window()
    first_window.show()
    sys.exit(app.exec_())
