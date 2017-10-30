#include "seasonplayersvm.h"

#include <QMessageBox>

#include "season.h"

const QStringList SeasonPlayersVM::_labelList = {"Last Name", "First Name", "Paid", "Playing Season"};
bool SeasonPlayersVM::_hide = false;
std::vector<SeasonPlayersVM::SeasonPlyrInfo> SeasonPlayersVM::_seasonVect;
int SeasonPlayersVM::_currSeason;

SeasonPlayersVM::SeasonPlayersVM(QObject *parent)
    :QAbstractTableModel(parent)
{
    for (int index = 0; index < Player::numRows(); index++)
    {
        SeasonPlyrInfo info;

        info.paid = false;
        info.inSeason = false;
        _seasonVect.push_back(info);
    }
}

int SeasonPlayersVM::rowCount(const QModelIndex &parent) const
{
    (void)parent;
    if (_hide)
    {
        // Some lesser count of rows
        return Player::numRows();
    }
    else
    {
        return Player::numRows();
    }
}

int SeasonPlayersVM::columnCount(const QModelIndex &parent) const
{
    (void)parent;
    return (_NUM_COLUMNS);
}

QVariant SeasonPlayersVM::data(const QModelIndex &index, int role) const
{
    switch (role)
    {
        case Qt::DisplayRole:
        {
            if (index.column() == _LAST_NAME_IDX) return Player::cell(index.row(), Player::_LAST_NAME_IDX);
            if (index.column() == _FIRST_NAME_IDX) return Player::cell(index.row(), Player::_FIRST_NAME_IDX);
            if (index.column() == _PAID_IDX)
            {
                return (Season::isPaid(_currSeason, index.row()) ? QString("t") : QString("f"));
            }
            if (index.column() == _IN_SEASON_IDX)
            {
                return (Season::isActPlyr(_currSeason, index.row()) ? QString("t") : QString("f"));
            }
            break;
        }
        case Qt::CheckStateRole:
        {
            if (index.column() == _PAID_IDX)
            {
                return (Season::isPaid(_currSeason, index.row()) ? Qt::Checked : Qt::Unchecked);
            }
            if (index.column() == _IN_SEASON_IDX)
            {
                return (Season::isActPlyr(_currSeason, index.row()) ? Qt::Checked : Qt::Unchecked);
            }
            break;
        }
    }
    return QVariant();
}

QVariant SeasonPlayersVM::headerData(int section, Qt::Orientation orientation, int role) const
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

Qt::ItemFlags SeasonPlayersVM::flags(const QModelIndex& index) const
{
    Qt::ItemFlags flags = 0;

    if ((index.column() == _PAID_IDX) || (index.column() == _IN_SEASON_IDX))
    {
        flags = Qt::ItemIsEnabled | Qt::ItemIsUserCheckable;
    }
    return (flags);
}

bool SeasonPlayersVM::setData(const QModelIndex & index, const QVariant & value, int role)
{
    if (role == Qt::CheckStateRole)
    {
        //save value from editor
        if (index.column() == _PAID_IDX)
        {
            bool update = false;
            if (value.toBool() == false)
            {
                QMessageBox::StandardButton reply;

                reply = QMessageBox::warning(nullptr, "Removing Paid",
                    "Removing paid flag, are you sure?", QMessageBox::Yes | QMessageBox::No);
                if (reply == QMessageBox::Yes)
                {
                    update = true;
                }
            }
            else
            {
                // If paid, player must also be playing the season
                Season::setActPlyr(_currSeason, index.row(), true);
                emit dataChanged(createIndex(index.row(), _IN_SEASON_IDX), createIndex(index.row(), _IN_SEASON_IDX));
                update = true;
            }
            if (update)
            {
                Season::setPaid(_currSeason, index.row(), (value.toBool() ? true: false));
            }
        }
        if (index.column() == _IN_SEASON_IDX)
        {
            bool update = false;
            if (value.toBool() == false)
            {
                // Check if paid is marked
                if (Season::isPaid(_currSeason, index.row()) == true)
                {
                    QMessageBox::warning(nullptr, "Removing Player from Season",
                        "Can't remove player from season if paid.");
                }
                else
                {
                    update = true;
                }
            }
            else
            {
                update = true;
            }
            if (update)
            {
                Season::setActPlyr(_currSeason, index.row(), (value.toBool() ? true: false));
            }
        }
    }
    return true;
}

void SeasonPlayersVM::setCurrSeason(int seasonUid)
{
    _currSeason = seasonUid;
}

void SeasonPlayersVM::addRow()
{
    beginInsertRows(QModelIndex(), Player::numRows() - 1, Player::numRows() - 1);
    endInsertRows();
}
