/********************************************************************************
** Form generated from reading UI file 'testWVGvOQ.ui'
**
** Created by: Qt User Interface Compiler version 5.15.11
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef TESTWVGVOQ_H
#define TESTWVGVOQ_H

#include "QtCharts/qchartglobal.h"
#include "QtCore/qobject.h"
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QFrame>
#include <QtWidgets/QLabel>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_CHARTS_USE_NAMESPACE
QT_BEGIN_NAMESPACE

class Ui_Form {
private:
  // basic ui elements
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
  QVBoxLayout *f5_chart_layout;

  // track previous button
  QPushButton *prev_button = nullptr;

  // values for k_buttons o change
  double k = 1.0;

  // chartview
  QChartView *chartView = nullptr;

  // on button click
  void on_button_clicked(QPushButton *clicked_button) {
    // set previous button to normal
    if (prev_button != nullptr) {
      prev_button->setStyleSheet("background-color: white");
    }
    // set current button to active
    clicked_button->setStyleSheet("background-color: blue");
    // set previous button to current clicked button
    prev_button = clicked_button;
    updateChart();
  }

public:
  // update chart
  void updateChart() {
    auto *series = new QLineSeries();
    for (int xPoint = 0; xPoint <= f5_inductor_slider->value(); ++xPoint) {
      double yPoint = k * xPoint * xPoint;
      *series << QPointF(xPoint, yPoint);
    }

    auto *chart = new QChart();
    chart->addSeries(series);
    chart->createDefaultAxes();
    chart->setTitle("y = k * x^2");

    // Set the range of y values from 0 to the square of the slider's value
    chart->axes(Qt::Vertical).first()->setRange(0, f5_inductor_slider->value());

    // Set the range of x values from 0 to the slider's value
    chart->axes(Qt::Horizontal)
        .first()
        ->setRange(0, f5_inductor_slider->value());

    // remove previous chartView
    if (chartView != nullptr) {
      f5_chart_layout->removeWidget(chartView);
      delete chartView;
    }
    // create new chartView
    chartView = new QChartView(chart);
    chartView->setSizePolicy(QSizePolicy::Expanding,
                             QSizePolicy::Expanding); // Set the size policy
    f5_chart_layout->addWidget(chartView);
  }

  // setupUi
  void setupUi(QWidget *Form) {
    if (Form->objectName().isEmpty()) {
      Form->setObjectName(QString::fromUtf8("Form"));
    }
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

    f5_k1_button = new QPushButton(frame_5);
    f5_k1_button->setObjectName(QString::fromUtf8("f5_k1_button"));
    f5_k1_button->setGeometry(QRect(80, 40, 80, 25));
    f5_k1_button->setStyleSheet("background-color: white");

    f5_k2_button = new QPushButton(frame_5);
    f5_k2_button->setObjectName(QString::fromUtf8("f5_k2_button"));
    f5_k2_button->setGeometry(QRect(170, 40, 80, 25));
    f5_k2_button->setStyleSheet("background-color: white");

    f5_k3_button = new QPushButton(frame_5);
    f5_k3_button->setObjectName(QString::fromUtf8("f5_k3_button"));
    f5_k3_button->setGeometry(QRect(260, 40, 80, 25));
    f5_k3_button->setStyleSheet("background-color: white");

    f5_fun1_button = new QPushButton(frame_5);
    f5_fun1_button->setObjectName(QString::fromUtf8("f5_fun1_button"));
    f5_fun1_button->setGeometry(QRect(350, 40, 80, 25));
    f5_fun1_button->setStyleSheet("background-color: white");

    f5_fun2_button = new QPushButton(frame_5);
    f5_fun2_button->setObjectName(QString::fromUtf8("f5_fun2_button"));
    f5_fun2_button->setGeometry(QRect(80, 70, 80, 25));
    f5_fun2_button->setStyleSheet("background-color: white");

    f5_fun3_button = new QPushButton(frame_5);
    f5_fun3_button->setObjectName(QString::fromUtf8("f5_fun3_button"));
    f5_fun3_button->setGeometry(QRect(170, 70, 80, 25));
    f5_fun3_button->setStyleSheet("background-color: white");

    f5_start_button = new QPushButton(frame_5);
    f5_start_button->setObjectName(QString::fromUtf8("f5_start_button"));
    f5_start_button->setGeometry(QRect(480, 80, 80, 25));
    f5_start_button->setStyleSheet("background-color: white");

    f5_inductor_slider = new QSlider(frame_5);
    f5_inductor_slider->setObjectName(QString::fromUtf8("f5_inductor_slider"));
    f5_inductor_slider->setGeometry(QRect(80, 130, 261, 16));
    f5_inductor_slider->setOrientation(Qt::Horizontal);
    f5_inductor_slider->setMinimum(0);
    f5_inductor_slider->setMaximum(10000);

    verticalLayoutWidget = new QWidget(frame_5);
    verticalLayoutWidget->setObjectName(
        QString::fromUtf8("verticalLayoutWidget"));
    verticalLayoutWidget->setGeometry(QRect(570, 20, 311, 181));

    f5_chart_layout = new QVBoxLayout(verticalLayoutWidget);
    f5_chart_layout->setObjectName(QString::fromUtf8("f5_chart_layout"));
    f5_chart_layout->setContentsMargins(0, 0, 0, 0);

    retranslateUi(Form);

    QMetaObject::connectSlotsByName(Form);

    // connect buttons to on_button_clicked
    QObject::connect(f5_k1_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_k1_button); });
    QObject::connect(f5_k2_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_k2_button); });
    QObject::connect(f5_k3_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_k3_button); });
    QObject::connect(f5_fun1_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_fun1_button); });
    QObject::connect(f5_fun2_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_fun2_button); });
    QObject::connect(f5_fun3_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_fun3_button); });
    QObject::connect(f5_start_button, &QPushButton::clicked,
                     [=]() { on_button_clicked(f5_start_button); });
    // connect slider to updateChart
    QObject::connect(f5_inductor_slider, &QSlider::valueChanged,
                     [=]() { updateChart(); });
  } // setupUi

  // retranslateUi
  void retranslateUi(QWidget *Form) const {
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

    f5_k1_button->setText(QCoreApplication::translate("Form", "k1", nullptr));
    f5_k2_button->setText(QCoreApplication::translate("Form", "k2", nullptr));
    f5_k3_button->setText(QCoreApplication::translate("Form", "k3", nullptr));
    f5_fun1_button->setText(
        QCoreApplication::translate("Form", "fun1", nullptr));
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

#endif // TESTWVGVOQ_H
