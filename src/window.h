#ifndef SRC_WINDOW_H
#define SRC_WINDOW_H

#include <memory>

#include <QMainWindow>
#include <QPushButton>
#include <QProgressBar>
#include <QSlider>

class Window : public QMainWindow {
  Q_OBJECT
public:
  explicit Window(QWidget* parent = NULL);

private slots:
  void handleButton();

private:
  std::unique_ptr<QPushButton> _push_button;
  std::unique_ptr<QProgressBar> _progress_bar;
  std::unique_ptr<QSlider> _slider;
};

#endif /* SRC_WINDOW_H */

