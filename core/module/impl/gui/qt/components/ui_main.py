# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(505, 300)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.drop_shadow_layout = QVBoxLayout(self.centralwidget)
        self.drop_shadow_layout.setSpacing(0)
        self.drop_shadow_layout.setObjectName(u"drop_shadow_layout")
        self.drop_shadow_layout.setContentsMargins(10, 10, 10, 10)
        self.drop_shadow_frame = QFrame(self.centralwidget)
        self.drop_shadow_frame.setObjectName(u"drop_shadow_frame")
        self.drop_shadow_frame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(238, 238, 236);\n"
"	border-radius: 10px;\n"
"}\n"
"")
        self.drop_shadow_frame.setFrameShape(QFrame.NoFrame)
        self.drop_shadow_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.drop_shadow_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header = QFrame(self.drop_shadow_frame)
        self.header.setObjectName(u"header")
        self.header.setMaximumSize(QSize(16777215, 30))
        self.header.setFrameShape(QFrame.StyledPanel)
        self.header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.header)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_spacer = QSpacerItem(387, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.header_spacer)

        self.controll_buttons = QFrame(self.header)
        self.controll_buttons.setObjectName(u"controll_buttons")
        self.controll_buttons.setMaximumSize(QSize(80, 30))
        self.controll_buttons.setFrameShape(QFrame.StyledPanel)
        self.controll_buttons.setFrameShadow(QFrame.Raised)
        self.controll_buttons.setMidLineWidth(1)
        self.horizontalLayout_2 = QHBoxLayout(self.controll_buttons)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.info_button = QPushButton(self.controll_buttons)
        self.info_button.setObjectName(u"info_button")
        self.info_button.setMaximumSize(QSize(30, 30))
        self.info_button.setStyleSheet(u"border: 0px;")
        icon = QIcon()
        icon.addFile(u"../gui/resources/icons/info-button.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.info_button.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.info_button)

        self.configurations_button = QPushButton(self.controll_buttons)
        self.configurations_button.setObjectName(u"configurations_button")
        self.configurations_button.setMaximumSize(QSize(30, 30))
        self.configurations_button.setStyleSheet(u"border: 0px;")
        icon1 = QIcon()
        icon1.addFile(u"../gui/resources/icons/gear.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.configurations_button.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.configurations_button)

        self.close_app_button = QPushButton(self.controll_buttons)
        self.close_app_button.setObjectName(u"close_app_button")
        self.close_app_button.setMaximumSize(QSize(30, 30))
        self.close_app_button.setStyleSheet(u"border: 0px;")
        icon2 = QIcon()
        icon2.addFile(u"../gui/resources/icons/remove-button.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_app_button.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.close_app_button)


        self.horizontalLayout.addWidget(self.controll_buttons)


        self.verticalLayout.addWidget(self.header)

        self.content = QFrame(self.drop_shadow_frame)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.StyledPanel)
        self.content.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.content)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.text_description_frame = QFrame(self.content)
        self.text_description_frame.setObjectName(u"text_description_frame")
        self.text_description_frame.setMaximumSize(QSize(16777215, 35))
        self.text_description_frame.setFrameShape(QFrame.StyledPanel)
        self.text_description_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.text_description_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(138, 14, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.text_description_frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout_5.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(137, 14, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.text_description_frame)

        self.voice_animation_dots_frame = QFrame(self.content)
        self.voice_animation_dots_frame.setObjectName(u"voice_animation_dots_frame")
        self.voice_animation_dots_frame.setMinimumSize(QSize(0, 50))
        self.voice_animation_dots_frame.setMaximumSize(QSize(16777215, 80))
        self.voice_animation_dots_frame.setFrameShape(QFrame.StyledPanel)
        self.voice_animation_dots_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.voice_animation_dots_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(154, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.voice_animation_dots_group = QFrame(self.voice_animation_dots_frame)
        self.voice_animation_dots_group.setObjectName(u"voice_animation_dots_group")
        self.voice_animation_dots_group.setMinimumSize(QSize(130, 50))
        self.voice_animation_dots_group.setMaximumSize(QSize(130, 80))
        self.voice_animation_dots_group.setFrameShape(QFrame.StyledPanel)
        self.voice_animation_dots_group.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.voice_animation_dots_group)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.dot_animation_dot_1 = QFrame(self.voice_animation_dots_group)
        self.dot_animation_dot_1.setObjectName(u"dot_animation_dot_1")
        self.dot_animation_dot_1.setMaximumSize(QSize(20, 20))
        self.dot_animation_dot_1.setStyleSheet(u"background-color: rgb(136, 138, 133);\n"
"border-radius: 10px;")
        self.dot_animation_dot_1.setFrameShape(QFrame.StyledPanel)
        self.dot_animation_dot_1.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.dot_animation_dot_1)

        self.dot_animation_dot_2 = QFrame(self.voice_animation_dots_group)
        self.dot_animation_dot_2.setObjectName(u"dot_animation_dot_2")
        self.dot_animation_dot_2.setMaximumSize(QSize(20, 20))
        self.dot_animation_dot_2.setStyleSheet(u"background-color: rgb(136, 138, 133);\n"
"border-radius: 10px;")
        self.dot_animation_dot_2.setFrameShape(QFrame.StyledPanel)
        self.dot_animation_dot_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.dot_animation_dot_2)

        self.dot_animation_dot_3 = QFrame(self.voice_animation_dots_group)
        self.dot_animation_dot_3.setObjectName(u"dot_animation_dot_3")
        self.dot_animation_dot_3.setMaximumSize(QSize(20, 20))
        self.dot_animation_dot_3.setStyleSheet(u"background-color: rgb(136, 138, 133);\n"
"border-radius: 10px;")
        self.dot_animation_dot_3.setFrameShape(QFrame.StyledPanel)
        self.dot_animation_dot_3.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.dot_animation_dot_3)

        self.dot_animation_dot_4 = QFrame(self.voice_animation_dots_group)
        self.dot_animation_dot_4.setObjectName(u"dot_animation_dot_4")
        self.dot_animation_dot_4.setMaximumSize(QSize(20, 20))
        self.dot_animation_dot_4.setStyleSheet(u"background-color: rgb(136, 138, 133);\n"
"border-radius: 10px;")
        self.dot_animation_dot_4.setFrameShape(QFrame.StyledPanel)
        self.dot_animation_dot_4.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.dot_animation_dot_4)


        self.horizontalLayout_4.addWidget(self.voice_animation_dots_group)

        self.horizontalSpacer_2 = QSpacerItem(154, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.voice_animation_dots_frame)

        self.text_input_frame = QFrame(self.content)
        self.text_input_frame.setObjectName(u"text_input_frame")
        self.text_input_frame.setFrameShape(QFrame.StyledPanel)
        self.text_input_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.text_input_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_5 = QSpacerItem(54, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_5)

        self.lineEdit = QLineEdit(self.text_input_frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(300, 0))
        self.lineEdit.setMaximumSize(QSize(300, 16777215))
        self.lineEdit.setStyleSheet(u"border-bottom: 1px solid #000;\n"
"border-radius: 0px;\n"
"background-color: rgba(255, 255, 255, 0);")

        self.horizontalLayout_6.addWidget(self.lineEdit)

        self.horizontalSpacer_6 = QSpacerItem(54, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.text_input_frame)


        self.verticalLayout.addWidget(self.content)


        self.drop_shadow_layout.addWidget(self.drop_shadow_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.info_button.setText("")
        self.configurations_button.setText("")
        self.close_app_button.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"How can i help you?", None))
    # retranslateUi

