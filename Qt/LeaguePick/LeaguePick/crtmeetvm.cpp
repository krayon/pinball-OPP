#include "crtmeetvm.h"

#include "season.h"
#include "player.h"
#include "groups.h"

#include "mainwindow.h"

const QStringList CrtMeetVM::_labelList = {"Last Name", "First Name", "Present"};
std::vector<CrtMeetVM::CrtMeetInfo> CrtMeetVM::_crtMeetVect;
int CrtMeetVM::_currSeason;
int CrtMeetVM::_state = CrtMeetVM::_STATE_NO_GRPS;
int CrtMeetVM::_addedPlyrs = 0;


CrtMeetVM::CrtMeetVM(QObject *parent)
    :QAbstractTableModel(parent)
{
    _currSeason = _ILLEGAL_MEET;
}

int CrtMeetVM::rowCount(const QModelIndex &parent) const
{
    (void)parent;

    // Count of players in this season
    return _crtMeetVect.size();
}

int CrtMeetVM::columnCount(const QModelIndex &parent) const
{
    (void)parent;
    return CrtMeetVM::_NUM_COLUMNS;
}

QVariant CrtMeetVM::data(const QModelIndex &index, int role) const
{
    switch (role)
    {
        case Qt::DisplayRole:
        {
            if (index.column() == _LAST_NAME_IDX) return Player::getLastName(_crtMeetVect[index.row()].playerUid);
            if (index.column() == _FIRST_NAME_IDX) return Player::getFirstName(_crtMeetVect[index.row()].playerUid);
            if (index.column() == _PRESENT_IDX) return (_crtMeetVect[index.row()].present ? QString("t") : QString("f"));
            break;
        }
        case Qt::CheckStateRole:
        {
            if (index.column() == _PRESENT_IDX)
            {
                return (_crtMeetVect[index.row()].present ? Qt::Checked : Qt::Unchecked);
            }
            break;
        }
    }
    return (QVariant());
}

QVariant CrtMeetVM::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role == Qt::DisplayRole)
    {
        if (orientation == Qt::Horizontal)
        {
            return (_labelList[section]);
        }
    }
    return QVariant();
}

Qt::ItemFlags CrtMeetVM::flags(const QModelIndex& index) const
{
    Qt::ItemFlags flags = 0;

    if (index.column() == _PRESENT_IDX)
    {
        if (_crtMeetVect[index.row()].disabled)
        {
            flags = Qt::ItemIsUserCheckable;
        }
        else
        {
            flags = Qt::ItemIsEnabled | Qt::ItemIsUserCheckable;
        }
    }
    return (flags);
}

bool CrtMeetVM::setData(const QModelIndex & index, const QVariant & value, int role)
{
    if (role == Qt::CheckStateRole)
    {
        _crtMeetVect[index.row()].present = value.toBool();
        if (_state == CrtMeetVM::_STATE_GRPS_CREATED)
        {
            // Adding a player
            if (value.toBool() == true)
            {
                _addedPlyrs++;
                if (_addedPlyrs <= Groups::_num3PlyrGrps)
                {
                    // Enable add late player button
                    // Disable finalize groups button
                    MainWindow::MainWin_p->updateGrpBtns(true, false);
                }
                else
                {
                    // Disable add late player button
                    // Disable finalize groups button
                    MainWindow::MainWin_p->updateGrpBtns(false, false);
                }
            }
            else
            {
                _addedPlyrs--;
                if (_addedPlyrs == 0)
                {
                    // Disable add late player button
                    // Enable finalize groups button
                    MainWindow::MainWin_p->updateGrpBtns(false, true);
                }
                else if (_addedPlyrs <= Groups::_num3PlyrGrps)
                {
                    // Enable add late player button
                    // Disable finalize groups button
                    MainWindow::MainWin_p->updateGrpBtns(true, false);
                }
            }
        }
    }
    return true;
}

void CrtMeetVM::updSeasonPlyr()
{
    _currSeason =  Season::currSeason;
    std::vector<int> actPlyrLst;
    std::vector<CrtMeetInfo> newVect;

    // Grab current player list for season
    actPlyrLst = Season::getActPlyrLst();

    for (auto &iter : actPlyrLst)
    {
        CrtMeetInfo tmpMeetInfo;

        tmpMeetInfo.playerUid = iter;
        if (_state == _STATE_NO_GRPS)
        {
            tmpMeetInfo.present = false;
            tmpMeetInfo.disabled = false;
        }
        else
        {
            for (auto &prevIter : _crtMeetVect)
            {
                if (prevIter.playerUid == iter)
                {
                    tmpMeetInfo.present = prevIter.present;
                    tmpMeetInfo.disabled = prevIter.disabled;
                    break;
                }
            }
        }
        newVect.push_back(tmpMeetInfo);
    }
    _crtMeetVect = newVect;
}

std::vector<int> CrtMeetVM::getPresentPlyrVect()
{
    std::vector<int> presentVect;

    for (auto &iter : _crtMeetVect)
    {
        if (iter.present)
        {
            iter.disabled = true;
            presentVect.push_back(iter.playerUid);
        }
    }
    _state = CrtMeetVM::_STATE_GRPS_CREATED;
    _addedPlyrs = 0;
    return (presentVect);
}

std::vector<int> CrtMeetVM::getLatePlyrVect()
{
    std::vector<int> lateVect;

    for (auto &iter : _crtMeetVect)
    {
        if (iter.present && !iter.disabled)
        {
            iter.disabled = true;
            lateVect.push_back(iter.playerUid);
        }
    }
    _addedPlyrs = 0;
    return (lateVect);
}

void CrtMeetVM::clearGroups()
{
    for (auto &iter : _crtMeetVect)
    {
        iter.disabled = false;
    }
    _state = CrtMeetVM::_STATE_NO_GRPS;
}
