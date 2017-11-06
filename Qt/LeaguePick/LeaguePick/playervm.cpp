#include "playervm.h"

#include "player.h"

const QStringList PlayerVM::_labelList = {"UID", "Last Name", "First Name", "Email", "Phone"};

PlayerVM::PlayerVM(QObject *parent)
    :QAbstractTableModel(parent)
{
}

int PlayerVM::rowCount(const QModelIndex &parent) const
{
    (void)parent;
    return Player::getNumPlyrs();
}

int PlayerVM::columnCount(const QModelIndex &parent) const
{
    (void)parent;
    return PlayerVM::_NUM_COLUMNS;
}

QVariant PlayerVM::data(const QModelIndex &index, int role) const
{
    switch (role)
    {
        case Qt::DisplayRole:
        case Qt::EditRole:
        {
            if (index.column() == _UID_IDX) return index.row();
            if (index.column() == _LAST_NAME_IDX) return Player::getLastName(index.row());
            if (index.column() == _FIRST_NAME_IDX) return Player::getFirstName(index.row());
            if (index.column() == _EMAIL_IDX) return Player::getEmail(index.row());
            if (index.column() == _PHONE_NUM_IDX) return Player::getPhone(index.row());
        }
    }
    return (QVariant());
}

QVariant PlayerVM::headerData(int section, Qt::Orientation orientation, int role) const
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

Qt::ItemFlags PlayerVM::flags(const QModelIndex& index) const
{
    Qt::ItemFlags flags = 0;

    // UID is not editable
    if (index.column() != _UID_IDX)
    {
        flags = Qt::ItemIsEnabled | Qt::ItemIsSelectable |  Qt::ItemIsEditable;
    }
    return (flags);
}

bool PlayerVM::setData(const QModelIndex & index, const QVariant & value, int role)
{
    if (role == Qt::EditRole)
    {
        //save value from editor
        if (index.column() == _LAST_NAME_IDX) Player::setLastName(index.row(), value.toString());
        if (index.column() == _FIRST_NAME_IDX) Player::setFirstName(index.row(), value.toString());
        if (index.column() == _EMAIL_IDX) Player::setEmail(index.row(), value.toString());
        if (index.column() == _PHONE_NUM_IDX) Player::setPhone(index.row(), value.toString());
    }
    return true;
}

void PlayerVM::addRow()
{
    beginInsertRows(QModelIndex(), Player::getNumPlyrs() - 1, Player::getNumPlyrs() - 1);
    endInsertRows();
}
