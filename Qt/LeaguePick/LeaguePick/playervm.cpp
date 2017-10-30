#include "playervm.h"

const QStringList PlayerVM::_labelList = {"UID", "Last Name", "First Name", "Email", "Phone"};

PlayerVM::PlayerVM(QObject *parent)
    :QAbstractTableModel(parent)
{
}

int PlayerVM::rowCount(const QModelIndex &parent) const
{
    (void)parent;
    return Player::numRows();
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
            if (index.column() == _UID_IDX) return Player::cell(index.row(), Player::_UID_IDX);
            if (index.column() == _LAST_NAME_IDX) return Player::cell(index.row(), Player::_LAST_NAME_IDX);
            if (index.column() == _FIRST_NAME_IDX) return Player::cell(index.row(), Player::_FIRST_NAME_IDX);
            if (index.column() == _EMAIL_IDX) return Player::cell(index.row(), Player::_EMAIL_IDX);
            if (index.column() == _PHONE_NUM_IDX) return Player::cell(index.row(), Player::_PHONE_NUM_IDX);
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
        if (index.column() == _LAST_NAME_IDX) Player::updCell(index.row(), Player::_LAST_NAME_IDX, value.toString());
        if (index.column() == _FIRST_NAME_IDX) Player::updCell(index.row(), Player::_FIRST_NAME_IDX, value.toString());
        if (index.column() == _EMAIL_IDX) Player::updCell(index.row(), Player::_EMAIL_IDX, value.toString());
        if (index.column() == _PHONE_NUM_IDX) Player::updCell(index.row(), Player::_PHONE_NUM_IDX, value.toString());
    }
    return true;
}

void PlayerVM::addRow()
{
    beginInsertRows(QModelIndex(), Player::numRows() - 1, Player::numRows() - 1);
    endInsertRows();
}
