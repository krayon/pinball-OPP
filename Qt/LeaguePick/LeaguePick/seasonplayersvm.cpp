#include "seasonplayersvm.h"

#include <QMessageBox>

#include "season.h"
#include "player.h"

#include "mainwindow.h"

const QStringList SeasonPlayersVM::_labelList = {"Last Name", "First Name", "Paid", "Playing Season"};
bool SeasonPlayersVM::_hide = false;
std::vector<SeasonPlayersVM::SeasonPlyrInfo> SeasonPlayersVM::_seasonVect;

SeasonPlayersVM::SeasonPlayersVM(QObject *parent)
    :QAbstractTableModel(parent)
{
    for (int index = 0; index < Player::getNumPlyrs(); index++)
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
        return Player::getNumPlyrs();
    }
    else
    {
        return Player::getNumPlyrs();
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
            if (index.column() == _LAST_NAME_IDX) return Player::getLastName(index.row());
            if (index.column() == _FIRST_NAME_IDX) return Player::getFirstName(index.row());
            if (index.column() == _PAID_IDX)
            {
                return (Season::isPaid(Season::currSeason, index.row()) ? QString(" ") : QString("  "));
            }
            if (index.column() == _IN_SEASON_IDX)
            {
                return (Season::isActPlyr(Season::currSeason, index.row()) ? QString(" ") : QString("  "));
            }
            break;
        }
        case Qt::CheckStateRole:
        {
            if (index.column() == _PAID_IDX)
            {
                return (Season::isPaid(Season::currSeason, index.row()) ? Qt::Checked : Qt::Unchecked);
            }
            if (index.column() == _IN_SEASON_IDX)
            {
                return (Season::isActPlyr(Season::currSeason, index.row()) ? Qt::Checked : Qt::Unchecked);
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
                Season::setActPlyr(Season::currSeason, index.row(), true);
                emit dataChanged(createIndex(index.row(), _IN_SEASON_IDX), createIndex(index.row(), _IN_SEASON_IDX));
                update = true;
            }
            if (update)
            {
                Season::setPaid(Season::currSeason, index.row(), (value.toBool() ? true: false));
            }
        }
        if (index.column() == _IN_SEASON_IDX)
        {
            bool update = false;
            if (value.toBool() == false)
            {
                // Check if paid is marked
                if (Season::isPaid(Season::currSeason, index.row()) == true)
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
                // Update the model and the create meet VM
                Season::setActPlyr(Season::currSeason, index.row(), (value.toBool() ? true: false));
                MainWindow::MainWin_p->updateSeasonPlayerVM();
            }
        }
    }
    return true;
}

void SeasonPlayersVM::addRow()
{
    beginInsertRows(QModelIndex(), Player::getNumPlyrs() - 1, Player::getNumPlyrs() - 1);
    endInsertRows();
}
