#include "crtmeetvm.h"

#include "season.h"

const QStringList CrtMeetVM::_labelList = {"Last Name", "First Name", "Present"};
std::vector<CrtMeetVM::CrtMeetInfo> CrtMeetVM::_crtMeetVect;
int CrtMeetVM::_currSeason;

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
        flags = Qt::ItemIsEnabled | Qt::ItemIsUserCheckable;
    }
    return (flags);
}

bool CrtMeetVM::setData(const QModelIndex & index, const QVariant & value, int role)
{
    if (role == Qt::CheckStateRole)
    {
        _crtMeetVect[index.row()].present = value.toBool();
    }
    return true;
}

void CrtMeetVM::updSeasonPlyr()
{
    _currSeason =  Season::currSeason;
    std::vector<int> actPlyrLst;

    // Grab current player list for season
    actPlyrLst = Season::getActPlyrLst();
    _crtMeetVect.clear();

    for (auto &iter : actPlyrLst)
    {
        CrtMeetInfo tmpMeetInfo;

        tmpMeetInfo.playerUid = iter;
        tmpMeetInfo.present = false;

        _crtMeetVect.push_back(tmpMeetInfo);
    }
}
