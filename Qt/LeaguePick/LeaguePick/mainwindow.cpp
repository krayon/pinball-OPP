#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QMenuBar>
#include <QMessageBox>
#include <QStringListModel>
#include <QSortFilterProxyModel>
#include <QComboBox>

#include "playervm.h"
#include "seasonplayersvm.h"
#include "player.h"
#include "season.h"

PlayerVM *plyrVM;
QSortFilterProxyModel proxyPlyrVM;
SeasonPlayersVM *seasonPlyrsVM;
QSortFilterProxyModel proxySeasonPlyrsVM;

void MainWindow::aboutLeaguePick()
{
    QMessageBox::information(this, "League Picker", "League Pick v00.00.00.01.");
}

void MainWindow::playerWindow()
{
}

void MainWindow::meetWindow()
{
}

void MainWindow::seasonWindow()
{
}

void MainWindow::addPlyrPush()
{
    bool ok;

    ok = Player::addPlayer(ui->lastNameEdit->text(), ui->firstNameEdit->text(),
        ui->phoneNumEdit->text(), ui->emailEdit->text());
    if (ok)
    {
        // May need to add another integer for bitfields
        Season::addPlyr();

        ui->lastNameEdit->setText("");
        ui->firstNameEdit->setText("");
        ui->phoneNumEdit->setText("");
        ui->emailEdit->setText("");
        plyrVM->addRow();
        seasonPlyrsVM->addRow();
    }
}

void MainWindow::addSeasonPush()
{
    bool ok;
    QString seasonName;
    int seasonUid;

    seasonName = ui->seasonNameEdit->text();
    ok = Season::addSeason(seasonName);
    if (ok)
    {
        seasonUid = Season::getUID(seasonName);
        ui->seasonCB->addItem(seasonName, seasonUid);
        ui->seasonCB->setCurrentIndex(ui->seasonCB->findText(seasonName));
        seasonPlyrsVM->setCurrSeason(seasonUid);
        ui->seasonNameEdit->setText("");
        ui->seasonPlyrView->reset();
    }
}

void MainWindow::editSeasonName()
{
    int seasonUID;

    seasonUID = ui->seasonCB->itemData(ui->seasonCB->currentIndex()).toInt();
    Season::updateName(seasonUID, ui->seasonCB->currentText());
}

void MainWindow::changeCurrSeason()
{
    int seasonUID;

    seasonUID = ui->seasonCB->itemData(ui->seasonCB->currentIndex()).toInt();
    seasonPlyrsVM->setCurrSeason(seasonUID);
    ui->seasonPlyrView->reset();
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    QMenu *helpMenu;
    QMenu *actionMenu;
    std::vector<Season::SeasonInfo> seasonVect;

    QAction *aboutLeaguePickAct = new QAction("About League Pick");
    QAction *playerAct = new QAction("Players");
    QAction *meetAct = new QAction("Meet");
    QAction *seasonAct = new QAction("Season");

    actionMenu = MainWindow::menuBar()->addMenu("Action");
    actionMenu->addAction(playerAct);
    actionMenu->addAction(meetAct);
    actionMenu->addAction(seasonAct);
    connect(playerAct, &QAction::triggered, this, &MainWindow::playerWindow);
    connect(meetAct, &QAction::triggered, this, &MainWindow::meetWindow);
    connect(seasonAct, &QAction::triggered, this, &MainWindow::seasonWindow);

    helpMenu = MainWindow::menuBar()->addMenu("Help");
    helpMenu->addAction(aboutLeaguePickAct);
    connect(aboutLeaguePickAct, &QAction::triggered, this, &MainWindow::aboutLeaguePick);
    ui->setupUi(this);

    Player::read();
    plyrVM = new PlayerVM(this);
    proxyPlyrVM.setSourceModel(plyrVM);

    ui->plyrTableView->setModel(&proxyPlyrVM);
    ui->plyrTableView->setSortingEnabled(true);
    ui->plyrTableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    connect(ui->addPlyrBtn, &QPushButton::clicked, this, &MainWindow::addPlyrPush);

    // Read season file and fill out combobox
    seasonVect = Season::read();
    for (auto &iter : seasonVect)
    {
        ui->seasonCB->addItem(iter.seasonName, iter.uid);
    }
    ui->seasonCB->setInsertPolicy(QComboBox::InsertAtCurrent);
    ui->seasonCB->setEditable(true);
    connect(ui->createSeasonBtn, &QPushButton::clicked, this, &MainWindow::addSeasonPush);
    connect(ui->seasonCB, &QComboBox::editTextChanged, this, &MainWindow::editSeasonName);
    connect(ui->seasonCB, &QComboBox::currentTextChanged, this, &MainWindow::changeCurrSeason);

    seasonPlyrsVM = new SeasonPlayersVM(this);
    proxySeasonPlyrsVM.setSourceModel(seasonPlyrsVM);

    ui->seasonPlyrView->setModel(&proxySeasonPlyrsVM);
    ui->seasonPlyrView->setSortingEnabled(true);
    ui->seasonPlyrView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::closeEvent (QCloseEvent *event)
{
    (void)event;

    // Update changes to player info
    if (Player::changesMade)
    {
        Player::write();
    }
    // Update changes to season info
    if (Season::changesMade)
    {
        Season::write();
    }
}
