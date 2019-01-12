#include "src/window.h"

#include <QApplication>
#include <QProgressBar>
#include <QPushButton>
#include <QSlider>

int main(int argc, char **argv) {
  QApplication app(argc, argv);

  Window window;
  window.setFixedSize(640, 384);
  window.grab().save("image.png");
}

