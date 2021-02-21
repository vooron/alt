# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_list_widget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ListWidget(object):
    def setupUi(self, ListWidget):
        if not ListWidget.objectName():
            ListWidget.setObjectName(u"ListWidget")
        ListWidget.resize(420, 190)
        ListWidget.setMinimumSize(QSize(420, 190))
        ListWidget.setMaximumSize(QSize(420, 190))
        self.verticalLayout_3 = QVBoxLayout(ListWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.drop_shadow_frame = QFrame(ListWidget)
        self.drop_shadow_frame.setObjectName(u"drop_shadow_frame")
        self.drop_shadow_frame.setMinimumSize(QSize(400, 170))
        self.drop_shadow_frame.setMaximumSize(QSize(400, 170))
        self.drop_shadow_frame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(238, 238, 236);\n"
"	border-radius: 15px;\n"
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
        self.close_app_button = QPushButton(self.controll_buttons)
        self.close_app_button.setObjectName(u"close_app_button")
        self.close_app_button.setMaximumSize(QSize(30, 30))
        self.close_app_button.setStyleSheet(u"border: 0px;")
        icon = QIcon()
        icon.addFile(u"resources/icons/remove-button.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.close_app_button.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.close_app_button)


        self.horizontalLayout.addWidget(self.controll_buttons)


        self.verticalLayout.addWidget(self.header)

        self.content = QFrame(self.drop_shadow_frame)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.StyledPanel)
        self.content.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.content)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.list = QListWidget(self.content)
        self.list.setObjectName(u"list")

        self.verticalLayout_2.addWidget(self.list)


        self.verticalLayout.addWidget(self.content)


        self.verticalLayout_3.addWidget(self.drop_shadow_frame)


        self.retranslateUi(ListWidget)

        QMetaObject.connectSlotsByName(ListWidget)
    # setupUi

    def retranslateUi(self, ListWidget):
        ListWidget.setWindowTitle(QCoreApplication.translate("ListWidget", u"Form", None))
        self.close_app_button.setText("")
    # retranslateUi

