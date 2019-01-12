#include "src/window.h"

using std::make_unique;

Window::Window(QWidget* parent) : QMainWindow(parent) {
  _push_button = make_unique<QPushButton>("Save Image", this);
  _push_button->setGeometry(10, 70, 80, 30);
  _progress_bar = make_unique<QProgressBar>(this);
  _progress_bar->setRange(0, 100);
  _progress_bar->setValue(0);
  _progress_bar->setGeometry(10, 10, 180, 30);
  _slider = make_unique<QSlider>(this);
  _slider->setOrientation(Qt::Horizontal);
  _slider->setRange(0, 100);
  _slider->setValue(0);
  _slider->setGeometry(10, 40, 180, 30);

  connect(_slider.get(), SIGNAL(valueChanged(int)), _progress_bar.get(),
          SLOT(setValue(int)));
  QObject::connect(_push_button.get(), SIGNAL(released()), this,
                   SLOT(handleButton()));
}

void Window::handleButton() {
  grab().save("image.png");
}

