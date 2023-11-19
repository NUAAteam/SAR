#include "testui.hpp"

int main(int argc, char *argv[]) {
  QApplication app(argc, argv);

  QWidget window;
  Ui_Form gui{};
  gui.setupUi(&window);
  window.show();
  gui.updateChart();

  return QApplication::exec();
}