/********************************************************************************
** Form generated from reading UI file 'testqGGiYD.ui'
**
** Created by: Qt User Interface Compiler version 5.15.11
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef TESTQGGIYD_H
#define TESTQGGIYD_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Form {
public:
  QFrame *frame_5;
  QLabel *f5_title_label;
  QLabel *f5_error_label;
  QLabel *f5_inductor_label;
  QPushButton *f5_k2_button;
  QPushButton *f5_k1_button;
  QPushButton *f5_fun1_button;
  QPushButton *f5_k3_button;
  QPushButton *f5_fun2_button;
  QPushButton *f5_fun3_button;
  QSlider *f5_inductor_slider;
  QPushButton *f5_start_button;
  QWidget *verticalLayoutWidget;
  QVBoxLayout *verticalLayout;

  void setupUi(QWidget *Form) {
    if (Form->objectName().isEmpty())
      Form->setObjectName(QString::fromUtf8("Form"));
    Form->resize(914, 247);
    frame_5 = new QFrame(Form);
    frame_5->setObjectName(QString::fromUtf8("frame_5"));
    frame_5->setGeometry(QRect(0, 10, 911, 231));
    frame_5->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    frame_5->setFrameShape(QFrame::StyledPanel);
    frame_5->setFrameShadow(QFrame::Raised);
    f5_title_label = new QLabel(frame_5);
    f5_title_label->setObjectName(QString::fromUtf8("f5_title_label"));
    f5_title_label->setGeometry(QRect(10, 10, 151, 17));
    f5_error_label = new QLabel(frame_5);
    f5_error_label->setObjectName(QString::fromUtf8("f5_error_label"));
    f5_error_label->setGeometry(QRect(10, 50, 54, 17));
    f5_inductor_label = new QLabel(frame_5);
    f5_inductor_label->setObjectName(QString::fromUtf8("f5_inductor_label"));
    f5_inductor_label->setGeometry(QRect(10, 130, 54, 17));
    f5_k2_button = new QPushButton(frame_5);
    f5_k2_button->setObjectName(QString::fromUtf8("f5_k2_button"));
    f5_k2_button->setGeometry(QRect(170, 40, 80, 25));
    f5_k2_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_k1_button = new QPushButton(frame_5);
    f5_k1_button->setObjectName(QString::fromUtf8("f5_k1_button"));
    f5_k1_button->setGeometry(QRect(80, 40, 80, 25));
    f5_k1_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_fun1_button = new QPushButton(frame_5);
    f5_fun1_button->setObjectName(QString::fromUtf8("f5_fun1_button"));
    f5_fun1_button->setGeometry(QRect(350, 40, 80, 25));
    f5_fun1_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_k3_button = new QPushButton(frame_5);
    f5_k3_button->setObjectName(QString::fromUtf8("f5_k3_button"));
    f5_k3_button->setGeometry(QRect(260, 40, 80, 25));
    f5_k3_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_fun2_button = new QPushButton(frame_5);
    f5_fun2_button->setObjectName(QString::fromUtf8("f5_fun2_button"));
    f5_fun2_button->setGeometry(QRect(80, 70, 80, 25));
    f5_fun2_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_fun3_button = new QPushButton(frame_5);
    f5_fun3_button->setObjectName(QString::fromUtf8("f5_fun3_button"));
    f5_fun3_button->setGeometry(QRect(170, 70, 80, 25));
    f5_fun3_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    f5_inductor_slider = new QSlider(frame_5);
    f5_inductor_slider->setObjectName(QString::fromUtf8("f5_inductor_slider"));
    f5_inductor_slider->setGeometry(QRect(80, 130, 261, 16));
    f5_inductor_slider->setOrientation(Qt::Horizontal);
    f5_start_button = new QPushButton(frame_5);
    f5_start_button->setObjectName(QString::fromUtf8("f5_start_button"));
    f5_start_button->setGeometry(QRect(480, 80, 80, 25));
    f5_start_button->setStyleSheet(
        QString::fromUtf8("QFrame, QLabel, QToolTip {\n"
                          "	background-color: rgb(255, 255, 255)\n"
                          "}"));
    verticalLayoutWidget = new QWidget(frame_5);
    verticalLayoutWidget->setObjectName(
        QString::fromUtf8("verticalLayoutWidget"));
    verticalLayoutWidget->setGeometry(QRect(570, 20, 311, 181));
    verticalLayout = new QVBoxLayout(verticalLayoutWidget);
    verticalLayout->setObjectName(QString::fromUtf8("verticalLayout"));
    verticalLayout->setContentsMargins(0, 0, 0, 0);

    retranslateUi(Form);

    QMetaObject::connectSlotsByName(Form);
  } // setupUi

  void retranslateUi(QWidget *Form) {
    Form->setWindowTitle(QCoreApplication::translate("Form", "Form", nullptr));
    f5_title_label->setText(QCoreApplication::translate(
        "Form",
        "\345\205\270\345\236\213\346\235\277\347\272\247\347\224\265\346\272"
        "\220\346\250\241\345\235\227\346\225\205\351\232\234\350\257\212\346"
        "\226\255",
        nullptr));
    f5_error_label->setText(QCoreApplication::translate(
        "Form", "\346\225\205\351\232\234\346\263\250\345\205\245:", nullptr));
    f5_inductor_label->setText(QCoreApplication::translate(
        "Form", "\347\224\265\346\204\237/mH", nullptr));
    f5_k2_button->setText(QCoreApplication::translate("Form", "k2", nullptr));
    f5_k1_button->setText(QCoreApplication::translate("Form", "k1", nullptr));
    f5_fun1_button->setText(
        QCoreApplication::translate("Form", "fun1", nullptr));
    f5_k3_button->setText(QCoreApplication::translate("Form", "k3", nullptr));
    f5_fun2_button->setText(
        QCoreApplication::translate("Form", "fun2", nullptr));
    f5_fun3_button->setText(
        QCoreApplication::translate("Form", "fun3", nullptr));
    f5_start_button->setText(QCoreApplication::translate(
        "Form", "\350\277\220\350\241\214", nullptr));
  } // retranslateUi
};

namespace Ui {
class Form : public Ui_Form {};
} // namespace Ui

QT_END_NAMESPACE

#endif // TESTQGGIYD_H
