#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui
{
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

    public:
        explicit MainWindow(QWidget *parent = 0);
        ~MainWindow();

    private:
        Ui::MainWindow *ui;

        void aboutLeaguePick();
        void playerWindow();
        void meetWindow();
        void seasonWindow();
        void closeEvent(QCloseEvent *event);
        void addPlyrPush();
        void addSeasonPush();
        void editSeasonName();
        void changeCurrSeason();
};

#endif // MAINWINDOW_H
