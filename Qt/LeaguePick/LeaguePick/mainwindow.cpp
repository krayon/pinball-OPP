#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QMenuBar>
#include <QMessageBox>
#include <QStringListModel>
#include <QSortFilterProxyModel>
#include <QComboBox>

#include <stdlib.h>
#include <time.h>

#include "player.h"
#include "season.h"
#include "last.h"
#include "meet.h"
#include "groups.h"

#include "playervm.h"
#include "seasonplayersvm.h"
#include "crtmeetvm.h"
#include "groupsvm.h"

#include "logfile.h"

PlayerVM *plyrVM;
QSortFilterProxyModel proxyPlyrVM;
SeasonPlayersVM *seasonPlyrsVM;
QSortFilterProxyModel proxySeasonPlyrsVM;
CrtMeetVM *crtMeetVM;
QSortFilterProxyModel proxyCrtMeetVM;
GroupsVM *groupsVM;
QSortFilterProxyModel proxyGroupsVM;
MainWindow *MainWindow::MainWin_p = nullptr;

void MainWindow::aboutLeaguePick()
{
    QMessageBox::information(this, "League Picker", "League Pick v00.00.00.01.");
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
        int newIndex;

        seasonUid = Season::getUID(seasonName);
        ui->seasonCB->addItem(seasonName, seasonUid);
        newIndex = ui->seasonCB->findText(seasonName);
        ui->seasonCB->setCurrentIndex(newIndex);
        ui->meetSeasonCB->addItem(seasonName, seasonUid);
        ui->meetSeasonCB->setCurrentIndex(newIndex);
        ui->meetGrpsSeasonCB->addItem(seasonName, seasonUid);
        ui->meetGrpsSeasonCB->setCurrentIndex(newIndex);
        Season::currSeason = seasonUid;
        ui->seasonNameEdit->setText("");
        ui->seasonPlyrView->reset();
    }
}

void MainWindow::editSeasonName()
{
    int seasonUID;

    seasonUID = ui->seasonCB->itemData(ui->seasonCB->currentIndex()).toInt();
    ui->meetSeasonCB->setItemText(seasonUID, ui->seasonCB->currentText());
    ui->meetGrpsSeasonCB->setItemText(seasonUID, ui->seasonCB->currentText());
    Season::updateName(seasonUID, ui->seasonCB->currentText());
}

void MainWindow::changeSeason(int seasonUID)
{
    std::vector<Meet::MeetInfo> meetVect;

    // Block the signals so this isn't called multiple to change
    // all three of the comboboxes.
    Season::currSeason = seasonUID;
    ui->seasonCB->blockSignals(true);
    ui->seasonCB->setCurrentIndex(seasonUID);
    ui->seasonCB->blockSignals(false);
    ui->meetSeasonCB->blockSignals(true);
    ui->meetSeasonCB->setCurrentIndex(seasonUID);
    ui->meetSeasonCB->blockSignals(false);
    ui->meetGrpsSeasonCB->blockSignals(true);
    ui->meetGrpsSeasonCB->setCurrentIndex(seasonUID);
    ui->meetGrpsSeasonCB->blockSignals(false);
    ui->seasonPlyrView->reset();
    updateSeasonPlayerVM();

    ui->meetGrpsNameCB->clear();
    meetVect = Meet::read();
    for (auto &iter : meetVect)
    {
        ui->meetGrpsNameCB->addItem(iter.meetName, iter.uid);
    }
}

void MainWindow::changeCurrSeason()
{
    int seasonUID;

    seasonUID = ui->seasonCB->itemData(ui->seasonCB->currentIndex()).toInt();
    changeSeason(seasonUID);
}

void MainWindow::meetSeasonChngSeason()
{
    int seasonUID;

    seasonUID = ui->meetSeasonCB->itemData(ui->meetSeasonCB->currentIndex()).toInt();
    changeSeason(seasonUID);
}

void MainWindow::meetGrpsChngSeason()
{
    int seasonUID;

    seasonUID = ui->meetGrpsSeasonCB->itemData(ui->meetGrpsSeasonCB->currentIndex()).toInt();
    changeSeason(seasonUID);
}

void MainWindow::crtGrpsPush()
{
    bool ok;
    QString meetName;
    int meetUid;

    meetName = ui->meetNameEdit->text();
    ok = Meet::addMeet(meetName);
    if (ok)
    {
        int newIndex;
        std::vector<int> presPlyrVect;

        meetUid = Meet::getUID(meetName);
        ui->meetGrpsNameCB->addItem(meetName, meetUid);
        newIndex = ui->meetGrpsNameCB->findText(meetName);
        ui->meetGrpsNameCB->blockSignals(true);
        ui->meetGrpsNameCB->setCurrentIndex(newIndex);
        ui->meetGrpsNameCB->blockSignals(false);

        Meet::currMeet = meetUid;
        ui->meetNameEdit->setText("");
        ui->meetGrpsView->reset();

        presPlyrVect = crtMeetVM->getPresentPlyrVect();
        Groups::createGroups(presPlyrVect);
        groupsVM->updMeet();
        proxyGroupsVM.setSourceModel(groupsVM);
    }
}

void MainWindow::meetGrpsChngMeet()
{
    int meetUid;

    meetUid = ui->meetGrpsNameCB->itemData(ui->meetGrpsNameCB->currentIndex()).toInt();
    if (meetUid != Meet::currMeet)
    {
        Meet::currMeet = meetUid;
        groupsVM->updMeet();
        proxyGroupsVM.setSourceModel(groupsVM);
    }
}

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    QMenu *helpMenu;
    std::vector<Season::SeasonInfo> seasonVect;
    std::vector<Meet::MeetInfo> meetVect;
    int lastSeason;
    int lastMeet;

    MainWin_p = this;

    // Initialize random seed using time
    srand (time(nullptr));

    QAction *aboutLeaguePickAct = new QAction("About League Pick");

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
        ui->meetSeasonCB->addItem(iter.seasonName, iter.uid);
        ui->meetGrpsSeasonCB->addItem(iter.seasonName, iter.uid);
    }
    ui->seasonCB->setInsertPolicy(QComboBox::InsertAtCurrent);
    ui->seasonCB->setEditable(true);
    connect(ui->createSeasonBtn, &QPushButton::clicked, this, &MainWindow::addSeasonPush);
    connect(ui->seasonCB, &QComboBox::editTextChanged, this, &MainWindow::editSeasonName);
    connect(ui->seasonCB, &QComboBox::currentTextChanged, this, &MainWindow::changeCurrSeason);
    connect(ui->meetSeasonCB, &QComboBox::currentTextChanged, this, &MainWindow::meetSeasonChngSeason);
    connect(ui->meetGrpsSeasonCB, &QComboBox::currentTextChanged, this, &MainWindow::meetGrpsChngSeason);

    seasonPlyrsVM = new SeasonPlayersVM(this);
    proxySeasonPlyrsVM.setSourceModel(seasonPlyrsVM);

    ui->seasonPlyrView->setModel(&proxySeasonPlyrsVM);
    ui->seasonPlyrView->setSortingEnabled(true);
    ui->seasonPlyrView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    crtMeetVM = new CrtMeetVM(this);
    proxyCrtMeetVM.setSourceModel(crtMeetVM);

    ui->meetPlyrView->setModel(&proxyCrtMeetVM);
    ui->meetPlyrView->setSortingEnabled(true);
    ui->meetPlyrView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
    connect(ui->createGrpsBtn, &QPushButton::clicked, this, &MainWindow::crtGrpsPush);

    groupsVM = new GroupsVM(this);
    proxyGroupsVM.setSourceModel(groupsVM);

    ui->meetGrpsView->setModel(&proxyGroupsVM);
    ui->meetGrpsView->setSortingEnabled(true);
    ui->meetGrpsView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    Last::read(lastSeason, lastMeet);
    if ((unsigned)lastSeason >= seasonVect.size())
    {
        QString errorStr("Last season value is invalid!");

        LogFile::write(errorStr);
        QMessageBox::critical(nullptr, "Last File season ID error", errorStr);
        exit (-1);
    }

    // Set season CB/currSeason and reset the view
    ui->seasonCB->setCurrentIndex(lastSeason);
    ui->meetSeasonCB->setCurrentIndex(lastSeason);
    ui->meetGrpsSeasonCB->setCurrentIndex(lastSeason);
    Season::currSeason = lastSeason;
    ui->seasonPlyrView->reset();
    crtMeetVM->updSeasonPlyr();
    proxyCrtMeetVM.setSourceModel(crtMeetVM);

    meetVect = Meet::read();
    for (auto &iter : meetVect)
    {
        ui->meetGrpsNameCB->addItem(iter.meetName, iter.uid);
    }
    ui->meetGrpsNameCB->setCurrentIndex(lastMeet);
    Meet::currMeet = lastMeet;

    // Read the groups data for the season
    Groups::read();
    groupsVM = new GroupsVM(this);
    groupsVM->updMeet();
    proxyGroupsVM.setSourceModel(groupsVM);

    connect(ui->meetGrpsNameCB, &QComboBox::currentTextChanged, this, &MainWindow::meetGrpsChngMeet);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::closeEvent (QCloseEvent *event)
{
    (void)event;

    // Update changes to players and seasons if necessary
    Player::write();
    Season::write();
    Last::write();
    Meet::write();
    Groups::write();
}

void MainWindow::updateSeasonPlayerVM()
{
    crtMeetVM->updSeasonPlyr();
    proxyCrtMeetVM.setSourceModel(crtMeetVM);
}
